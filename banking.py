import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

conn.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);')

INSERT_DATA_NUMBER_PIN = 'INSERT INTO card (number, pin) VALUES (?, ?);'
GET_NUMBER_PIN_DATA = 'SELECT number, pin FROM card'
GET_DATA_NUMBER_PIN = 'SELECT number, pin FROM card'


def add_data_number_pin(conn, number, pin):
    with conn:
        return conn.execute(INSERT_DATA_NUMBER_PIN, (number, pin)).fetchone()


def get_number_pin_data(conn):
    with conn:
        return conn.execute(GET_NUMBER_PIN_DATA).fetchall()


def get_balance(conn):
    with conn:
        return conn.execute(GET_BALANCE).fetchone()


# def add_income(conn):
#     with conn:
#         return conn.execute(ADD_INCOME).fetchone()

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
            input_income = input('\nEnter income: ')
            ADD_INCOME = 'UPDATE card SET balance = "%s" WHERE number = "%s"' % (input_income, input_card_number)
            conn.execute(ADD_INCOME).fetchone()
            add_income(conn, input_card_number)
            conn.commit()
            print('Income was added!')
        if choice == 3:
            pass
        if choice == 4:
            pass
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
