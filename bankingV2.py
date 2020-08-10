# NOTE: This version includes the Luhn Algorithm to verify that the card number is real...
# Luhn checks if all of the sum of digits modulo 10 == 0
# Write your code here
import random
import string


class Banking:
    def __init__(self):
        self.balance = 0
        self.list_digits = string.digits
        self.list_accounts = {}
        self.prompt = ("1. Create an account\n2. Log into account\n0. Exit")
        self.bank_num = ['4', '0', '0', '0', '0', '0']

    def create_acc(self):
        account_number = random.choices(self.list_digits, k=9)
        list_card_num = self.bank_num + account_number
        card_number = ''.join(list_card_num)
        checksum = self.luhn_algo(card_number)
        card_number_checksum = card_number + checksum
        pin = ''.join(random.choices(self.list_digits, k=4))
        self.list_accounts[card_number_checksum] = pin
        print("Your card has been created\nYour card number:\n" +
              card_number_checksum)
        print("Your card PIN:\n" + pin)

    def luhn_algo(self, card_num):
        double_everyother_digit = []
        for index, value in enumerate(card_num):
            if index % 2 == 0:
                val_2 = int(value)*2
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
        if self.list_accounts.get(card_num_inp) == pin_num_inp:
            print("Successfully logged in!")
            while True:
                choice2 = input("1. Balance\n2. Log Out\n0. Exit")
                if choice2 == '1':
                    print(f"Balance: {self.balance}")
                if choice2 == '2':
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
