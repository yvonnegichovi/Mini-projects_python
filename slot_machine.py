#!/usr/bin/python3

import random

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}

class Profile:
    def __init__(self, name, balance=100):
        self.name = name
        self.balance = balance

    def __str__(self):
        return f"Profile: {self.name}, Balance: ${self.balance}"
    def deposit(self):
        while True:
            amount = input("What would you like to deposit? $")
            if amount.isdigit():
                amount = int(amount)
                if amount > 0:
                    break
                else:
                    print("Amount must be greater than 0.")
            else:
                print("Please enter a number.")
        self.balance += amount

class SlotMachine:
    def __init__(self):
        self.profiles = []
    def create_profile(self, name, initial_balance=100):
        profile = Profile(name, initial_balance)
        self.profiles.append(profile)
        return profile
    def display_profiles(self):
        for profile in self.profiles:
            print(profile)

    def check_winnings(self, columns, lines, bet, values):
        winnings = 0
        winning_lines = []
        for line in range(lines):
            symbol = columns[0][line]
            for column in columns:
                symbol_to_check = column[line]
                if symbol != symbol_to_check:
                    break
            else:
                winnings = values[symbol] * bet
                winning_lines.append(lines + 1)

        return winnings, winning_lines

    def get_slot_machine_spin(self, rows, cols, symbols):
        all_symbols = []
        for symbol, symbol_count in symbols.items():
            for _ in range(symbol_count):
                all_symbols.append(symbol)
        columns = []
        for col in range(cols):
            column = []
            current_symbols = all_symbols[:]
            for row in range(rows):
                value = random.choice(current_symbols)
                current_symbols.remove(value)
                column.append(value)
            columns.append(column)

        return columns

    def print_slot_machine(self, columns):
        for row in range(len(columns[0])):
            for i, column in enumerate(columns):
                if i != len(columns) - 1:
                    print(column[row], end=" | ")
                else:
                    print(column[row], end="")
            print()


    def get_number_of_lines(self):
        while True:
            lines = input("Enter the number of lines to bet on(1-" + str(MAX_LINES) + ")? ")
            if lines.isdigit():
                lines = int(lines)
                if 1 <= lines <= MAX_LINES:
                    break
                else:
                    print("Enter a valid number of lines.")
            else:
                print("Please enter a number.")
        return lines

    def get_bet(self):
        while True:
            amount = input("What would you like to bet on each line? $")
            if amount.isdigit():
                amount = int(amount)
                if MIN_BET <= amount <= MAX_BET:
                    break
                else:
                    print(f"Amount must be between ${MIN_BET} - ${MAX_BET}.")
            else:
                print("Please enter a number.")
        return amount

    def spin(self, profile):
        deposit_answer = input("Do you want to make a deposit? (y/n): ").lower()
        if deposit_answer == "y":
            self.deposit(profile)
        lines = self.get_number_of_lines()
        while True:
            bet = self.get_bet()
            total_bet = bet * lines
            if total_bet > profile.balance:
                print(f"You do not have enough to bet that amount, your current balance is: ${balance}")
            else:
                break
        print(f"You are betting ${bet} on {lines} lines. Total bet is equal to ${total_bet}")
        slots = self.get_slot_machine_spin(ROWS, COLS, symbol_count)
        self.print_slot_machine(slots)
        winnings, winning_lines = self.check_winnings(slots, lines, bet, symbol_value)
        print(f"You won ${winnings}.")
        print(f"You won on lines:", *winning_lines)
        profile.balance += winnings - total_bet

    def main(self):
        slot_machine = SlotMachine()
        while True:
            profile_name = input("Enter your profile name (q to quit): ")
            if profile_name.lower() == "q":
                break
            initial_balance = int(input("Enter the initial balance for the profile: "))
            player_profile = slot_machine.create_profile(profile_name, initial_balance)
            deposit_answer = input("Do you want to make a deposit? (y/n): ").lower()
            if deposit_answer == "y":
                player_profile.deposit()
            while True:
                print(player_profile)
                answer = input("Press enter to play (q to quit).")
                if answer.lower() == "q":
                    print(f"{player_profile.name}, thank you for playing. Time for the next player.")
                    break
                self.spin(player_profile)

        self.display_profiles()
if __name__ == "__main__":
    slot_machine = SlotMachine()
    slot_machine.main()
