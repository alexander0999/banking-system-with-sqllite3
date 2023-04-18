import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

conn.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);')

INSERT_DATA_NUMBER_PIN = 'INSERT INTO card (number, pin) VALUES (?, ?);'
GET_NUMBER_PIN_DATA = 'SELECT number, pin FROM card'
GET_DATA_NUMBER_PIN = 'SELECT number, pin FROM card'
GET_OTHER_CARD_NUMBER = 'SELECT ALL number FROM card'


def add_data_number_pin(conn, number, pin):
    with conn:
        return conn.execute(INSERT_DATA_NUMBER_PIN, (number, pin)).fetchone()


def get_number_pin_data(conn):
    with conn:
        return conn.execute(GET_NUMBER_PIN_DATA).fetchall()


def get_balance(conn, input_card_number):
    with conn:
        return conn.execute(GET_BALANCE).fetchone()


def remove_money_transfer(conn, REMOVE_MONEY_TRANSFER):
    with conn:
        return conn.execute(REMOVE_MONEY_TRANSFER).fetchone()


def add_money_transfer(conn, ADD_MONEY_TRANSFER):
    with conn:
        return conn.execute(ADD_MONEY_TRANSFER).fetchone()


def get_other_card_number(conn):
    with conn:
        return conn.execute(GET_OTHER_CARD_NUMBER).fetchall()


def luhn_algorithm(card):
    card = list(card)
    for i in range(len(card)):  # translate all elements to int
        card[i] = int(card[i])
    for i in range(0, len(card), 2):  # multiply odd by 2
        card[i] *= 2
    for i in range(len(card)):  # minus 9 from elements > 9
        if card[i] >= 10:
            card[i] = card[i] - 9
    while True:
        check_digit = random.randint(0, 9)
        sum_elements = sum(card) + check_digit
        if sum_elements % 10 == 0:
            last_element = check_digit
            return last_element


def check_luhn_algorithm(check):
    check_card = list(check)
    check_card_last_elem = int(check_card.pop(-1))
    for i in range(len(check_card)):  # translate all elements to int
        check_card[i] = int(check_card[i])
    for i in range(0, len(check_card), 2):  # multiply odd by 2
        check_card[i] *= 2
    for i in range(len(check_card)):  # minus 9 from elements > 9
        if check_card[i] >= 10:
            check_card[i] = check_card[i] - 9
    while True:
        sum_elements = sum(check_card) + check_card_last_elem
        if sum_elements % 10 == 0:
            return True
        else:
            return False


def account_identifier():
    account_identifier = str()
    while len(account_identifier) < 9:
        account_identifier = str(random.randint(000000000, 999999999))
    account_identifier = '400000' + str(account_identifier)
    return account_identifier


def create_pincode():
    pincode = str()
    while len(pincode) < 4:
        pincode = str(random.randint(0000, 9999))
    return pincode


def account(input_card_number):
    while True:
        print('\n1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit')
        choice = int(input())
        if choice == 1:
            balance = get_balance(conn)
            print('\nBalance: ' + str(balance[0]))
        if choice == 2:
            def add_income(conn, input_card_number):
                with conn:
                    return conn.execute(ADD_INCOME).fetchone()
            input_income = int(input('\nEnter income: '))
            prev_balance_tuple = get_balance(conn, input_card_number)
            prev_balance = prev_balance_tuple[0]
            new_balanace = prev_balance + input_income
            ADD_INCOME = 'UPDATE card SET balance = "%s" WHERE number = "%s"' % (new_balanace, input_card_number)
            conn.execute(ADD_INCOME).fetchone()
            add_income(conn, input_card_number)
            conn.commit()
            print('Income was added!')
        if choice == 3:
            card_numbers_touple = get_other_card_number(conn)
            card_numbers_list = []
            for i in range(0, len(card_numbers_touple)):
                card_numbers_list.append(card_numbers_touple[i][0])
            transfer_card_number = str(input('\nTransfer\nEnter card number:\n'))
            if transfer_card_number != str(input_card_number):
                if check_luhn_algorithm(transfer_card_number) == True:
                    if transfer_card_number in card_numbers_list:
                            transfer_money = int(input('Enter how much money you want to transfer:\n'))
                            check_balance = get_balance(conn, input_card_number)
                            GET_BALANCE_TRANSFER = 'SELECT balance FROM card WHERE number = "%s"' % transfer_card_number
                            def get_balance_transfer(conn):
                                # get balance of transfer card
                                with conn:
                                    return conn.execute(GET_BALANCE_TRANSFER).fetchone()
                            check_balance_transfer = get_balance_transfer(conn)
                            if transfer_money < check_balance[0]:
                                new_balance_main = check_balance[0] - transfer_money
                                REMOVE_MONEY_TRANSFER = 'UPDATE card SET balance = "%s" WHERE number = "%s"' % (new_balance_main, input_card_number)
                                remove_money_transfer(conn, REMOVE_MONEY_TRANSFER)
                                new_balance_transfer = check_balance_transfer[0] + transfer_money
                                ADD_MONEY_TRANSFER = 'UPDATE card SET balance = "%s" WHERE number = "%s"' % (new_balance_transfer, transfer_card_number)
                                add_money_transfer(conn, ADD_MONEY_TRANSFER)
                                print('\nSuccess!')
                            else:
                                print('Not enough money!')
                    else:
                        print('Such a card does not exist.')
                else:
                    print('Probably you made a mistake in the card number. Please try again!')
            else:
                print("You can't transfer money to the same account!")
        if choice == 4:
            def close_account(conn, input_card_number):
                with conn:
                    return conn.execute(CLOSE_ACCOUNT).fetchone()

            CLOSE_ACCOUNT = 'DELETE FROM card WHERE number = "%s"' % input_card_number

            close_account(conn, input_card_number)
            conn.commit()
            print('\nThe account has been closed!\n')
            break
        if choice == 5:
            print('\nYou have successfully logged out!\n')
            break
        if choice == 0:
            print('\nBye!')
            exit()


while True:
    print('1. Create an account\n2. Log into account\n0. Exit')

    choice = int(input())

    if choice == 1:
        temp_card_number = account_identifier()
        user_card_number = str(temp_card_number) + str(luhn_algorithm(temp_card_number))
        user_pincode = create_pincode()
        add_data_number_pin(conn, user_card_number, user_pincode)  # запись в бд
        conn.commit()
        print(f'\nYour card has been created\nYour card number:\n{int(user_card_number)}\nYour card PIN:\n{int(user_pincode)}\n')
    if choice == 2:
        input_card_number = int(input('\nEnter your card number:\n'))
        input_card_pincode = int(input('Enter your PIN:\n'))
        clients = (get_number_pin_data(conn))
        input_tuple = (str(input_card_number), str(input_card_pincode))  # for checking in bd
        GET_BALANCE = 'SELECT balance FROM card WHERE number = "%s"' % input_card_number  # sql querry for balance
        if input_tuple in clients:
            print('\nYou have successfully logged in!')
            account(input_card_number)
        else:
            print('\nWrong card number or PIN!\n')
    if choice == 0:
        print('\nBye!')
        exit()
