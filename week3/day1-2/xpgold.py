class BankAccount:
    def __init__(self,balance,username,passwaord,authenticated=False):
        self.balance = balance
        self.username = username
        self.password = passwaord
        self.authenticated = authenticated
    def deposit(self, amount):
        if not self.authenticated:
            raise Exception("Authentication required to perform this action.")
        if amount <0:
            raise Exception("Deposit amount must be positive")
        self.balance += amount
    def withdraw(self, amount):
        if not self.authenticated:
            raise Exception("Authentication required to perform this action.")
        if amount <0:
            raise Exception("Withdrawal amount must be positive")
        if amount > self.balance:
            print("Insufficient funds, withdrawal denied.")
        else:
            self.balance -= amount
    def authenticate(self, username, password):
        if self.username == username and self.password == password:
            self.authenticated = True
            print("Authentication successful.")
        else:
            self.authenticated = False
            print("Authentication failed. Incorrect username or password.")
            
class MinimumBalanceAccount(BankAccount):
    def __init__(self, balance, minimum_balance=0):
        super().__init__(balance)
        self.minimum_balance = minimum_balance
    def withdraw(self, amount):
        if self.balance<self.minimum_balance:
            raise Exception("Account balance is below the minimum required balance. Withdrawal denied.")
        super().withdraw(amount)

'''
Part IV: BONUS Create an ATM class

__init__:
Accepts the following parameters: account_list and try_limit.

Validates that account_list contains a list of BankAccount or MinimumBalanceAccount instances.
Hint: isinstance()

Validates that try_limit is a positive number, if you get an invalid input raise an Exception, then move along and set try_limit to 2.
Hint: Check out this tutorial

Sets attribute current_tries = 0

Call the method show_main_menu (see below)

Methods:
show_main_menu:
This method will start a while loop to display a menu letting a user select:
Log in : Will ask for the users username and password and call the log_in method with the username and password (see below).
Exit.

log_in:
Accepts a username and a password.

Checks the username and the password against all accounts in account_list.
If there is a match (ie. use the authenticate method), call the method show_account_menu.
If there is no match with any existing accounts, increment the current tries by 1. Continue asking the user for a username and a password, until the limit is reached (ie. try_limit attribute). Once reached display a message saying they reached max tries and shutdown the program.

show_account_menu:
Accepts an instance of BankAccount or MinimumBalanceAccount.
The method will start a loop giving the user the option to deposit, withdraw or exit.'''

class ATM:
    def __init__(self, account_list, try_limit):
        if not all(isinstance(account, (BankAccount, MinimumBalanceAccount)) for account in account_list):
            raise Exception("account_list must contain only BankAccount or MinimumBalanceAccount instances.")
        if try_limit <= 0:
            print("Invalid try limit. Setting try limit to 2.")
            self.try_limit = 2
        else:
            self.try_limit = try_limit
        self.account_list = account_list
        self.current_tries = 0
        self.show_main_menu()
    