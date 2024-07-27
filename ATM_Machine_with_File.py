import random as rd
import json

User_Accounts = {"-1234": {"Name": "", "Pin": 0, "balance": 999}}
Accounts = []

# Load accounts from file
def load_accounts():
    global User_Accounts, Accounts
    try:
        with open('accounts.json', 'r') as file:
            User_Accounts = json.load(file)
            Accounts = [int(account) for account in User_Accounts.keys()]
    except FileNotFoundError:
        pass

# Save accounts to file
def save_accounts():
    with open('accounts.json', 'w') as file:
        json.dump(User_Accounts, file)

# Log transaction
def log_transaction(account_number, transaction):
    with open(f'{account_number}_transactions.txt', 'a') as file:
        file.write(transaction + '\n')

def add_customer():
    account_number = 0
    name = ''
    pin = 0
    deposit_amount = 0.0

    while True:
        account_number = rd.randint(1000, 9999)
        if account_number not in Accounts:
            Accounts.append(account_number)
            break

    name = input("Please enter your name: ")
    print(f"Your account number is: {account_number}")

    while True:
        pin = input("Please enter your 4 digit pin: ")
        repin = input("Re-enter your 4 digit pin: ")
        if len(pin) == 4 and pin.isdigit() and  pin == repin:
            pin = int(pin)
            print("Pin created")
            break
        elif len(pin) != 4 or not pin.isdigit():
            print("Entered pin is not 4 digits, try again")
        else:
            print("Entered pin does not match, try again")

    while True:
        deposit_amount = int(input("Enter your deposit amount (min Rs.500.00, max Rs.9999999): "))
        if deposit_amount < 500.00 or deposit_amount > 9999999:
            print("Please deposit within the stipulated amount, try again")
        else:
            print(f"Rs.{deposit_amount} is deposited into your account {account_number}")
            break

    new_account = {"Name": name, "Pin": pin, "balance": deposit_amount}
    User_Accounts[str(account_number)] = new_account
    save_accounts()
    log_transaction(account_number, f"Account created with initial deposit: Rs.{deposit_amount}")

    print(f"Your details are\n Name: {name}\nAccount Number: {account_number}\nBalance: {deposit_amount}\n")

    return account_number, pin

def deposit(account_number, deposit_amount):
    temp_account_number = str(account_number)
    User_Accounts[temp_account_number]['balance'] += deposit_amount
    while True:
        if User_Accounts[temp_account_number]['balance'] > 9999999:
            User_Accounts[temp_account_number]['balance'] -= deposit_amount
            print("The deposited amount increases the account balance beyond Rs.9999999\nMoney will be returned\n")
            break
        else:
            save_accounts()
            log_transaction(account_number, f"Deposited Rs.{deposit_amount}")
            print(f"Deposited Rs.{deposit_amount} successfully\nCurrent balance is Rs.{User_Accounts[temp_account_number]['balance']}\n")
            break

def withdraw(account_number, withdraw_amount):
    temp_account_number = str(account_number)
    User_Accounts[temp_account_number]['balance'] -= withdraw_amount
    while True:
        if User_Accounts[temp_account_number]['balance'] < 500:
            User_Accounts[temp_account_number]['balance'] += withdraw_amount
            print("The withdrawn amount will decrease the account balance below Rs.500.00\nMoney will be returned\n")
            break
        else:
            save_accounts()
            log_transaction(account_number, f"Withdrew Rs.{withdraw_amount}")
            print(f"Withdrew Rs.{withdraw_amount} successfully\nCurrent balance is Rs.{User_Accounts[temp_account_number]['balance']}\n")
            break

def Balance_Inquiry(account_number):
    print(f"Current balance is Rs.{User_Accounts[str(account_number)]['balance']}\n")

def Change_PIN(account_number):
    new_pin = 0
    while True:
        new_pin = int(input("Please enter your 4 digit pin: "))
        new_repin = int(input("Re-enter your 4 digit pin: "))
        if new_pin == new_repin:
            User_Accounts[str(account_number)]['Pin'] = new_pin
            save_accounts()
            print("Pin Updated\n")
            break
        else:
            print("Entered pin is wrong, try again\n")

def view_transaction_history(account_number):
    try:
        with open(f'{account_number}_transactions.txt', 'r') as file:
            print(f"Transaction history for account {account_number}:")
            print(file.read())
    except FileNotFoundError:
        print("No transaction history found.")

# Main program
load_accounts()

choice = 0
count = 3
login_count = 0    
account_number = 0
pin = 0



while True:
    User_input = input("New Member, yes or no: ")
    if User_input in ['Yes', 'yes', 'YES']:
        account_number, pin = add_customer()
    
    while(True):

            
            while (True):
                print("Please enter Account details:")
                account_number = int(input())
                
                if account_number not in Accounts:
                    print("You have entered an invalid Account number, please try again")
                else:
                    while(True):
                        pin = int(input("Enter your 4 digit PIN number: "))
                        if User_Accounts[str(account_number)]['Pin'] == pin:
                            print("Welcome")
                            
                            while(True):
                                print("Press 1 for Account balance inquiry")
                                print("Press 2 for Cash withdrawal")
                                print("Press 3 for Cash Deposit")
                                print("Press 4 for PIN change")
                                print("Press 5 for Transaction History")
                                print("Press 6 to end the session")
                                print("Press 7 to exit the application")
                                choice = int(input("\n Enter your choice:"))
                                
                                if choice == 1:
                                    Balance_Inquiry(account_number)
                                elif choice == 2:
                                    withdraw_amount = int(input("Enter withdraw amount:"))
                                    withdraw(account_number, withdraw_amount)
                                elif choice == 3:
                                    deposit_amount = int(input("Enter deposit amount:"))
                                    deposit(account_number, deposit_amount)
                                elif choice == 4:
                                    Change_PIN(account_number)
                                elif choice == 5:
                                    view_transaction_history(account_number)
                                elif choice == 6:
                                    print("Thank You")
                                    break
                                elif choice == 7:
                                    exit(0)

                            break
                        if count == 0:
                            print("You have exceeded your pin entries, your card is locked. Please contact any branch office")
                            exit(0)
                        else:
                            print(f"You have entered an invalid pin, please try again. You have {count} tries remaining")
                            count -= 1
                        
                
        

