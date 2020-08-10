# Includes fully fleshed out system once you log in like "Depositing Money" or "Transferring money"

import random
import string
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
# Creating table 'card' and executing other SQL Queries
cur.execute("DROP TABLE card")
cur.execute('CREATE TABLE IF NOT EXISTS card(id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')
# Saving the changes we made!
conn.commit()


class Banking:
    def __init__(self):
        self.balance = 0
        self.list_digits = string.digits
        self.prompt = "1. Create an account\n2. Log into account\n0. Exit"
        self.bank_num = ['4', '0', '0', '0', '0', '0']

    def create_acc(self):
        account_number = random.choices(self.list_digits, k=9)
        list_card_num = self.bank_num + account_number
        card_number = ''.join(list_card_num)
        checksum = self.luhn_algo(card_number)
        card_number_checksum = card_number + checksum
        pin = ''.join(random.choices(self.list_digits, k=4))
        cur.execute("INSERT INTO card(number, pin, balance) VALUES (?,?,?)",
                    (card_number_checksum, pin, 0))
        conn.commit()
        print("Your card has been created\nYour card number:\n" +
              card_number_checksum)
        print("Your card PIN:\n" + pin)

    def luhn_algo(self, card_num):
        # Returns the checksum of a credit card (last digit) that satisfies the mod 10 requirement
        double_everyother_digit = []
        for index, value in enumerate(card_num):
            if index % 2 == 0:
                val_2 = int(value) * 2
                if val_2 > 9:
                    doubled_subtract_nine = val_2 - 9
                    double_everyother_digit.append(doubled_subtract_nine)
                else:
                    double_everyother_digit.append(val_2)
            else:
                double_everyother_digit.append(int(value))
        return str(sum(double_everyother_digit) * 9 % 10)

    def log_acc(self):
        card_num_inp = input("Enter your card number:\n")
        pin_num_inp = input("Enter your PIN:\n")
        cur.execute("SELECT * FROM card WHERE number = ? AND pin = ?",
                    (card_num_inp, pin_num_inp))
        account = cur.fetchone()
        if account:
            print("Successfully logged in!")
            while True:
                choice2 = input(
                    "1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log Out\n0. Exit")
                if choice2 == '1':  # Balance
                    print(f"Balance: {account[3]}")

                if choice2 == '2':  # Add income
                    income = input("Enter income:\n")
                    cur.execute(
                        "UPDATE card SET balance = ? + balance WHERE number = ?", (income, card_num_inp))
                    conn.commit()
                    print("Income was added!")
                    cur.execute(
                        "SELECT * FROM card WHERE number = ?", [card_num_inp])
                    account = cur.fetchone()

                if choice2 == '3':  # Do Transfer
                    acc_deposit_into = input("Transfer\nEnter card number: ")
                    str_acc_deposit_into = ''.join(acc_deposit_into)
                    luhn_algo_check_sum = self.luhn_algo(
                        str_acc_deposit_into[:-1])
                    if luhn_algo_check_sum == str_acc_deposit_into[-1]:
                        cur.execute(
                            "SELECT * FROM card WHERE number = ?", [acc_deposit_into])
                        account2 = cur.fetchone()
                        if account2:
                            if account2[1] == card_num_inp:
                                print(
                                    "You can't transfer money to the same account dummy")
                                break
                            withdraw = input(
                                "Enter how much money you want to transfer: ")
                            if int(withdraw) > account[3]:
                                print("Not enough money!")
                            else:
                                cur.execute(
                                    "UPDATE card SET balance = balance + ? WHERE number = ?", (withdraw, acc_deposit_into))
                                cur.execute(
                                    "UPDATE card SET balance = balance - ? WHERE number = ?", (withdraw, card_num_inp))
                                conn.commit()
                                cur.execute(
                                    "SELECT * FROM card WHERE number = ?", [card_num_inp])
                                account = cur.fetchone()
                                print("Success!")
                        else:
                            print("Such a card does not exist.")
                    else:
                        print(
                            "You probably made a mistake in the card number. Please try again!")

                if choice2 == '4':  # Close account
                    cur.execute(
                        "DELETE FROM card WHERE number = ?", [card_num_inp])
                    conn.commit()
                    print("The account has been closed!")

                if choice2 == '5':  # Log out
                    print("Successfully logged out!")
                    break

                if choice2 == '0':
                    self.exit()
        else:
            print("Wrong Card number or PIN!")

    def exit(self):
        print("Bye!")
        quit()


if __name__ == "__main__":
    bank = Banking()
    while True:
        choice = input(bank.prompt)
        if choice == '1':  # Create an account
            bank.create_acc()
        if choice == '2':  # Log into account
            bank.log_acc()
        if choice == "0":  # Exit
            bank.exit()
