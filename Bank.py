import os

Transaction_file = "transaction.txt"
account_file = "account.txt"

class Bankaccount:
    def __init__(self):
        self.account_holder = input("Enter holder name :").strip()

        while True:
            acc_num_str = input("Enter account number :").strip()
            if not acc_num_str.isdigit():
                print("Invalid account number. Please enter digits only.")
                continue
            acc_num = int(acc_num_str)
            if self.is_account_number_taken(acc_num):
                print("Account number already exists. Please choose a different account number.")
            else:
                self.account_number = acc_num
                break

        while True:
            try:
                self.balance = float(input("Enter balance :").strip())
                break
            except ValueError:
                print("Invalid amount. Please enter a numeric balance.")

        self.password = input("Set your accout password:").strip()

        self.log_transaction("Account created", self.balance)
        self.save_account()

    def save_account(self):
        try:
            with open(account_file, "a") as file:
                file.write(
                    f"{self.account_holder},{self.account_number},{self.balance},{self.password}\n"
                )
        except IOError:
            print("Error saving account.")

    def update_account(self):
        lines = []
        found = False

        if os.path.exists(account_file):
            with open(account_file, "r") as file:
                lines = file.readlines()

        with open(account_file, "w") as file:
            for line in lines:
                data = line.strip().split(",")

                if len(data) >= 2 and data[1] == str(self.account_number):
                    file.write(
                        f"{self.account_holder},{self.account_number},{self.balance},{self.password}\n"
                    )
                    found = True
                else:
                    file.write(line)

            if not found:
                file.write(
                    f"{self.account_holder},{self.account_number},{self.balance},{self.password}\n"
                )

    def debit(self, amount):
        if amount <= 0:
            print("Invalid amount")
        elif amount > self.balance:
            print("Insufficient funds")
        else:
            self.balance -= amount
            self.update_account()
            self.log_transaction("Debit", amount)
            print("Rs", amount, "was debited")
            print("Total Balance is!", "Rs", self.get_balance())

    def credit(self, amount):
        if amount <= 0:
            print("Invalid amount")
        else:
            self.balance += amount
            self.update_account()
            self.log_transaction("Credit", amount)
            print("Rs", amount, "was credited")
            print("Total Balance is!", "Rs", self.get_balance())

    def get_balance(self):
        return self.balance

    def log_transaction(self, transaction_type, amount):
        try:
            with open(Transaction_file, "a") as file:
                log_string = (
                    f"Holder: {self.account_holder} | "
                    f"Acc No: {self.account_number} | "
                    f"Type: {transaction_type} | "
                    f"Amount: Rs {amount} | "
                    f"Updated Balance: Rs {self.balance}\n"
                )
                file.write(log_string)
        except IOError:
            print("Error: Unable to write to the transaction log file.")

    @staticmethod
    def load_account(account_number, password):
        if not os.path.exists(account_file):
            return None

        with open(account_file, "r") as file:
            for line in file:
                data = line.strip().split(",")

                if len(data) == 4:
                    holder, acc, balance, pwd = data

                    if acc == account_number and pwd == password:
                        account = Bankaccount.__new__(Bankaccount)

                        account.account_holder = holder
                        account.account_number = int(acc)
                        account.balance = float(balance)
                        account.password = pwd

                        return account

        return None

    @staticmethod
    def is_account_number_taken(account_number):
        if not os.path.exists(account_file):
            return False
        with open(account_file, "r") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) >= 2 and data[1] == str(account_number):
                    return True
        return False


def main():
    print("Welcome to the Bank Account Management System!")

    while True:
        print("\n1. Create Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            Bankaccount()
        elif choice == "2":
            acc = input("Account number: ")
            pwd = input("Password: ")

            account = Bankaccount.load_account(acc, pwd)

            if account:
                print("Login Successful")

                while True:
                    print("\nBanking Operations")
                    print("1. Debit")
                    print("2. Credit")
                    print("3. Check Balance")
                    print("4. Logout")

                    choice = input("Enter your choice: ")

                    if choice == "1":
                        try:
                            amount = float(input("Enter amount: "))
                            account.debit(amount)
                        except ValueError:
                            print("Invalid amount.")

                    elif choice == "2":
                        try:
                            amount = float(input("Enter amount: "))
                            account.credit(amount)
                        except ValueError:
                            print("Invalid amount.")

                    elif choice == "3":
                        print("Current Balance: Rs", account.get_balance())

                    elif choice == "4":
                        print("Logged out successfully.")
                        break

                    else:
                        print("Invalid choice.")

            else:
                print("Invalid account number or password")

if __name__ == "__main__":
    main()

Holder: varn | Acc No: 25202020065 | Type: Account created | Amount: Rs 536453746.0 | Updated Balance: Rs 536453746.0
Holder: varn | Acc No: 25202020065 | Type: Credit | Amount: Rs 2534347.0 | Updated Balance: Rs 538988093.0
Holder: arjun | Acc No: 25202020076 | Type: Account created | Amount: Rs 536673.0 | Updated Balance: Rs 536673.0
Holder: varun | Acc No: 25202020087 | Type: Account created | Amount: Rs 5676536736.0 | Updated Balance: Rs 5676536736.0

varn,25202020065,538988093.0,1234
arjun,25202020076,536673.0,1234
varun,25202020087,5676536736.0,1234

