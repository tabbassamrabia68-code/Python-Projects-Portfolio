"""
==============================================================================
 PROJECT      : Bank Management System
 DESCRIPTION  : A console-based Bank Management System built using Python OOP
                concepts with JSON file storage for persistent data.
 AUTHOR       : Rabia Tabbassam
 GITHUB       : https://github.com/tabbassamrabia68-code
 LINKEDIN     : https://www.linkedin.com/in/rabia-tabbassam/
==============================================================================
"""

# ------------------------------------------------------------------------
# IMPORTS
# ------------------------------------------------------------------------
import json                # For reading/writing account data in JSON format
import os                  # For checking whether the data file exists
from datetime import datetime  # For timestamping every transaction


# ------------------------------------------------------------------------
# GLOBAL CONSTANTS
# ------------------------------------------------------------------------
DATA_FILE = "accounts.json"        # File where all account data is stored
STARTING_ACCOUNT_NUMBER = 1001     # First auto-generated account number


# ==========================================================================
# CLASS: Account
# --------------------------------------------------------------------------
# Represents a single bank account. Stores personal details, balance,
# and a full transaction history for that account.
# ==========================================================================
class Account:

    def __init__(self, account_number, full_name, cnic, phone_number,
                 balance=0.0, transaction_history=None):
        self.account_number = account_number
        self.full_name = full_name
        self.cnic = cnic
        self.phone_number = phone_number
        self.balance = balance
        # If no history is passed (new account), start with an empty list
        self.transaction_history = transaction_history if transaction_history else []

    # ----------------------------------------------------------------
    # Adds a new transaction record to this account's history.
    # Every deposit, withdrawal, or transfer calls this method.
    # ----------------------------------------------------------------
    def add_transaction(self, transaction_type, amount):
        transaction_record = {
            "type": transaction_type,
            "amount": round(amount, 2),
            "balance_after": round(self.balance, 2),
            "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.transaction_history.append(transaction_record)

    # ----------------------------------------------------------------
    # Converts this Account object into a dictionary so it can be
    # saved into the JSON file.
    # ----------------------------------------------------------------
    def to_dict(self):
        return {
            "account_number": self.account_number,
            "full_name": self.full_name,
            "cnic": self.cnic,
            "phone_number": self.phone_number,
            "balance": self.balance,
            "transaction_history": self.transaction_history
        }

    # ----------------------------------------------------------------
    # Creates an Account object back from a dictionary (used when
    # loading data from the JSON file).
    # ----------------------------------------------------------------
    @staticmethod
    def from_dict(data):
        return Account(
            account_number=data["account_number"],
            full_name=data["full_name"],
            cnic=data["cnic"],
            phone_number=data["phone_number"],
            balance=data["balance"],
            transaction_history=data["transaction_history"]
        )


# ==========================================================================
# CLASS: Bank
# --------------------------------------------------------------------------
# Manages the entire collection of accounts. Handles creation, searching,
# deposits, withdrawals, transfers, deletion, and JSON persistence.
# ==========================================================================
class Bank:

    def __init__(self):
        # Dictionary of all accounts -> { "ACC1001": Account object, ... }
        self.accounts = {}
        self.load_data()

    # ======================================================================
    # SECTION: JSON FILE HANDLING (Load / Save)
    # ======================================================================

    # ----------------------------------------------------------------
    # Loads account data from the JSON file when the program starts.
    # If the file does not exist or is empty/corrupted, starts fresh.
    # ----------------------------------------------------------------
    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as file:
                    raw_data = json.load(file)
                    for acc_number, acc_data in raw_data.items():
                        self.accounts[acc_number] = Account.from_dict(acc_data)
            except (json.JSONDecodeError, ValueError):
                # File exists but is empty or corrupted -> start with no accounts
                self.accounts = {}
            except Exception as error:
                print(f"⚠️  Unexpected error while loading data: {error}")
                self.accounts = {}
        else:
            # No file yet -> this is the first time the program is run
            self.accounts = {}

    # ----------------------------------------------------------------
    # Saves all current account data to the JSON file.
    # Called automatically after every change (deposit, withdraw, etc.)
    # ----------------------------------------------------------------
    def save_data(self):
        try:
            with open(DATA_FILE, "w") as file:
                data_to_save = {
                    acc_number: account.to_dict()
                    for acc_number, account in self.accounts.items()
                }
                json.dump(data_to_save, file, indent=4)
        except Exception as error:
            print(f"❌ Error saving data: {error}")

    # ======================================================================
    # SECTION: HELPER / VALIDATION FUNCTIONS
    # ======================================================================

    # ----------------------------------------------------------------
    # Generates the next available account number in the format
    # ACC1001, ACC1002, ACC1003, ...
    # ----------------------------------------------------------------
    def generate_account_number(self):
        if not self.accounts:
            next_number = STARTING_ACCOUNT_NUMBER
        else:
            # Extract the numeric part of every account number, find the max, add 1
            existing_numbers = [
                int(acc_number.replace("ACC", ""))
                for acc_number in self.accounts.keys()
            ]
            next_number = max(existing_numbers) + 1

        return f"ACC{next_number}"

    # ----------------------------------------------------------------
    # Validates that the name contains only alphabets and spaces.
    # ----------------------------------------------------------------
    @staticmethod
    def is_valid_name(name):
        name = name.strip()
        return name != "" and all(char.isalpha() or char.isspace() for char in name)

    # ----------------------------------------------------------------
    # Validates that CNIC contains exactly 13 digits (dashes allowed
    # in user input but stripped before validation/storage).
    # ----------------------------------------------------------------
    @staticmethod
    def is_valid_cnic(cnic):
        cleaned_cnic = cnic.replace("-", "").strip()
        return cleaned_cnic.isdigit() and len(cleaned_cnic) == 13

    # ----------------------------------------------------------------
    # Validates that phone number contains 10 or 11 digits.
    # ----------------------------------------------------------------
    @staticmethod
    def is_valid_phone(phone):
        phone = phone.strip()
        return phone.isdigit() and len(phone) in (10, 11)

    # ----------------------------------------------------------------
    # Validates that a deposit/withdraw/transfer amount is a positive number.
    # ----------------------------------------------------------------
    @staticmethod
    def is_valid_amount(amount_str):
        try:
            amount = float(amount_str)
            return amount > 0
        except ValueError:
            return False

    # ----------------------------------------------------------------
    # Checks if a CNIC already exists in the system (prevents duplicates).
    # ----------------------------------------------------------------
    def is_duplicate_cnic(self, cnic):
        cleaned_cnic = cnic.replace("-", "").strip()
        for account in self.accounts.values():
            if account.cnic == cleaned_cnic:
                return True
        return False

    # ----------------------------------------------------------------
    # Finds and returns an Account object by account number, or None.
    # ----------------------------------------------------------------
    def find_account(self, account_number):
        return self.accounts.get(account_number.strip().upper())

    # ======================================================================
    # SECTION: FEATURE 1 - CREATE ACCOUNT
    # ======================================================================
    def create_account(self):
        print("\n----- CREATE NEW ACCOUNT -----")

        # ---- Validate Full Name ----
        full_name = input("Enter Full Name: ").strip()
        while not self.is_valid_name(full_name):
            print("❌ Invalid name. Only alphabets and spaces are allowed.")
            full_name = input("Enter Full Name: ").strip()

        # ---- Validate CNIC (and check duplicates) ----
        cnic = input("Enter CNIC (13 digits): ").strip()
        while not self.is_valid_cnic(cnic):
            print("❌ Invalid CNIC. It must contain exactly 13 digits.")
            cnic = input("Enter CNIC (13 digits): ").strip()

        cleaned_cnic = cnic.replace("-", "")
        if self.is_duplicate_cnic(cleaned_cnic):
            print("❌ An account with this CNIC already exists. Account creation cancelled.")
            return

        # ---- Validate Phone Number ----
        phone_number = input("Enter Phone Number (10 or 11 digits): ").strip()
        while not self.is_valid_phone(phone_number):
            print("❌ Invalid phone number. It must contain 10 or 11 digits.")
            phone_number = input("Enter Phone Number (10 or 11 digits): ").strip()

        # ---- Validate Initial Deposit ----
        initial_deposit_str = input("Enter Initial Deposit Amount: ").strip()
        while not (initial_deposit_str.replace(".", "", 1).isdigit()):
            print("❌ Invalid amount. Please enter a valid number.")
            initial_deposit_str = input("Enter Initial Deposit Amount: ").strip()
        initial_deposit = float(initial_deposit_str)

        # ---- Generate Account Number and Create Account Object ----
        new_account_number = self.generate_account_number()
        new_account = Account(
            account_number=new_account_number,
            full_name=full_name,
            cnic=cleaned_cnic,
            phone_number=phone_number,
            balance=initial_deposit
        )

        # ---- Record the initial deposit as the first transaction ----
        if initial_deposit > 0:
            new_account.add_transaction("Initial Deposit", initial_deposit)

        # ---- Save the new account and persist data ----
        self.accounts[new_account_number] = new_account
        self.save_data()

        print("\n✅ Account created successfully!")
        print(f"   Account Number : {new_account_number}")
        print(f"   Full Name      : {full_name}")
        print(f"   Balance        : {initial_deposit:.2f}")

    # ======================================================================
    # SECTION: FEATURE 2 - VIEW ALL ACCOUNTS
    # ======================================================================
    def view_all_accounts(self):
        print("\n----- ALL ACCOUNTS -----")

        if not self.accounts:
            print("No accounts found in the system.")
            return

        # ---- Print table header ----
        print(f"{'Account No.':<12}{'Full Name':<22}{'Phone Number':<15}{'Balance':<12}")
        print("-" * 61)

        # ---- Print each account as a table row ----
        for account in self.accounts.values():
            print(f"{account.account_number:<12}{account.full_name:<22}"
                  f"{account.phone_number:<15}{account.balance:<12.2f}")

    # ======================================================================
    # SECTION: FEATURE 3 - SEARCH ACCOUNT
    # ======================================================================
    def search_account(self):
        print("\n----- SEARCH ACCOUNT -----")
        account_number = input("Enter Account Number (e.g., ACC1001): ").strip().upper()
        account = self.find_account(account_number)

        if account is None:
            print("❌ No account found with this account number.")
            return

        print("\n✅ Account Found:")
        print(f"   Account Number : {account.account_number}")
        print(f"   Full Name      : {account.full_name}")
        print(f"   CNIC           : {account.cnic}")
        print(f"   Phone Number   : {account.phone_number}")
        print(f"   Balance        : {account.balance:.2f}")

    # ======================================================================
    # SECTION: FEATURE 4 - DEPOSIT MONEY
    # ======================================================================
    def deposit_money(self):
        print("\n----- DEPOSIT MONEY -----")
        account_number = input("Enter Account Number: ").strip().upper()
        account = self.find_account(account_number)

        if account is None:
            print("❌ Account not found.")
            return

        amount_str = input("Enter Amount to Deposit: ").strip()
        if not self.is_valid_amount(amount_str):
            print("❌ Invalid amount. Deposit amount must be a positive number.")
            return

        amount = float(amount_str)

        # ---- Update balance and record transaction ----
        account.balance += amount
        account.add_transaction("Deposit", amount)
        self.save_data()

        print(f"✅ Deposit successful! New Balance: {account.balance:.2f}")

    # ======================================================================
    # SECTION: FEATURE 5 - WITHDRAW MONEY
    # ======================================================================
    def withdraw_money(self):
        print("\n----- WITHDRAW MONEY -----")
        account_number = input("Enter Account Number: ").strip().upper()
        account = self.find_account(account_number)

        if account is None:
            print("❌ Account not found.")
            return

        amount_str = input("Enter Amount to Withdraw: ").strip()
        if not self.is_valid_amount(amount_str):
            print("❌ Invalid amount. Withdrawal amount must be a positive number.")
            return

        amount = float(amount_str)

        # ---- Check for sufficient balance before withdrawing ----
        if amount > account.balance:
            print("❌ Insufficient balance for this withdrawal.")
            return

        # ---- Update balance and record transaction ----
        account.balance -= amount
        account.add_transaction("Withdraw", amount)
        self.save_data()

        print(f"✅ Withdrawal successful! New Balance: {account.balance:.2f}")

    # ======================================================================
    # SECTION: FEATURE 6 - CHECK BALANCE
    # ======================================================================
    def check_balance(self):
        print("\n----- CHECK BALANCE -----")
        account_number = input("Enter Account Number: ").strip().upper()
        account = self.find_account(account_number)

        if account is None:
            print("❌ Account not found.")
            return

        print(f"💰 Current Balance for {account.full_name} ({account.account_number}): "
              f"{account.balance:.2f}")

    # ======================================================================
    # SECTION: FEATURE 7 - TRANSFER MONEY
    # ======================================================================
    def transfer_money(self):
        print("\n----- TRANSFER MONEY -----")

        sender_account_number = input("Enter Sender Account Number: ").strip().upper()
        sender_account = self.find_account(sender_account_number)
        if sender_account is None:
            print("❌ Sender account not found.")
            return

        receiver_account_number = input("Enter Receiver Account Number: ").strip().upper()
        receiver_account = self.find_account(receiver_account_number)
        if receiver_account is None:
            print("❌ Receiver account not found.")
            return

        # ---- Prevent transferring to the same account ----
        if sender_account_number == receiver_account_number:
            print("❌ Sender and receiver accounts cannot be the same.")
            return

        amount_str = input("Enter Amount to Transfer: ").strip()
        if not self.is_valid_amount(amount_str):
            print("❌ Invalid amount. Transfer amount must be a positive number.")
            return

        amount = float(amount_str)

        # ---- Check sender has sufficient balance ----
        if amount > sender_account.balance:
            print("❌ Insufficient balance in sender's account.")
            return

        # ---- Perform the transfer ----
        sender_account.balance -= amount
        receiver_account.balance += amount

        # ---- Record transaction for BOTH accounts ----
        sender_account.add_transaction(
            f"Transfer Sent to {receiver_account_number}", amount
        )
        receiver_account.add_transaction(
            f"Transfer Received from {sender_account_number}", amount
        )

        self.save_data()

        print(f"✅ Transfer successful! {amount:.2f} sent from "
              f"{sender_account_number} to {receiver_account_number}.")
        print(f"   Sender New Balance   : {sender_account.balance:.2f}")
        print(f"   Receiver New Balance : {receiver_account.balance:.2f}")

    # ======================================================================
    # SECTION: FEATURE 8 - DELETE ACCOUNT
    # ======================================================================
    def delete_account(self):
        print("\n----- DELETE ACCOUNT -----")
        account_number = input("Enter Account Number to Delete: ").strip().upper()
        account = self.find_account(account_number)

        if account is None:
            print("❌ Account not found.")
            return

        # ---- Ask for confirmation before permanently deleting ----
        confirmation = input(
            f"Are you sure you want to delete account of '{account.full_name}' "
            f"({account_number})? This action cannot be undone. (yes/no): "
        ).strip().lower()

        if confirmation == "yes":
            del self.accounts[account_number]
            self.save_data()
            print("✅ Account deleted successfully.")
        else:
            print("❌ Account deletion cancelled.")

    # ======================================================================
    # SECTION: FEATURE 9 - TRANSACTION HISTORY
    # ======================================================================
    def view_transaction_history(self):
        print("\n----- TRANSACTION HISTORY -----")
        account_number = input("Enter Account Number: ").strip().upper()
        account = self.find_account(account_number)

        if account is None:
            print("❌ Account not found.")
            return

        if not account.transaction_history:
            print("No transactions have been made on this account yet.")
            return

        print(f"\nTransaction History for {account.full_name} ({account.account_number})")
        print(f"{'Type':<28}{'Amount':<12}{'Balance After':<15}{'Date & Time'}")
        print("-" * 80)

        for transaction in account.transaction_history:
            print(f"{transaction['type']:<28}{transaction['amount']:<12.2f}"
                  f"{transaction['balance_after']:<15.2f}{transaction['date_time']}")


# ==========================================================================
# FUNCTION: display_menu
# --------------------------------------------------------------------------
# Displays the main console menu of the Bank Management System.
# ==========================================================================
def display_menu():
    print("""
==========================================
        BANK MANAGEMENT SYSTEM
==========================================
1. Create Account
2. View All Accounts
3. Search Account
4. Deposit Money
5. Withdraw Money
6. Check Balance
7. Transfer Money
8. Delete Account
9. Transaction History
10. Exit
==========================================
""")


# ==========================================================================
# FUNCTION: main
# --------------------------------------------------------------------------
# The main program loop. Creates the Bank object (which auto-loads data),
# displays the menu, and routes user choices to the correct feature.
# ==========================================================================
def main():
    bank = Bank()   # Automatically loads existing data from accounts.json

    while True:
        display_menu()

        try:
            user_choice = input("Enter your choice (1-10): ").strip()
        except KeyboardInterrupt:
            # Handles Ctrl+C gracefully by saving data before exiting
            print("\n\n⚠️  Program interrupted. Saving data before exit...")
            bank.save_data()
            break

        # ---- Route the user's choice to the correct Bank method ----
        try:
            if user_choice == "1":
                bank.create_account()
            elif user_choice == "2":
                bank.view_all_accounts()
            elif user_choice == "3":
                bank.search_account()
            elif user_choice == "4":
                bank.deposit_money()
            elif user_choice == "5":
                bank.withdraw_money()
            elif user_choice == "6":
                bank.check_balance()
            elif user_choice == "7":
                bank.transfer_money()
            elif user_choice == "8":
                bank.delete_account()
            elif user_choice == "9":
                bank.view_transaction_history()
            elif user_choice == "10":
                # ---- Save all data one final time before exiting ----
                bank.save_data()
                print("\n👋 All data saved. Thank you for using the "
                      "Bank Management System. Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter a number between 1 and 10.")

        except Exception as error:
            # ---- Catches any unexpected error so the program never crashes ----
            print(f"⚠️  An unexpected error occurred: {error}")


# ------------------------------------------------------------------------
# ENTRY POINT
# ------------------------------------------------------------------------
if __name__ == "__main__":
    main()
