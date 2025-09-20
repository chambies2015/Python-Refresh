from datetime import datetime, timedelta
import csv
import json

class Bank:
    def __init__(self):
        self.bank_accounts = {}
        self.ledger = []

    def create_account(self, name, account_type=None):
        if account_type == "checking":
            account = CheckingAccount(name)
        elif account_type == "savings":
            account = SavingsAccount(name)
        else:
            account = BankAccount(name)

        account._bank = self
        self.bank_accounts[name] = account

    def get_account(self, name):
        return self.bank_accounts.get(name)

    def transfer(self, from_name, to_name, amount):
        from_account = self.bank_accounts.get(from_name)
        to_account = self.bank_accounts.get(to_name)

        if from_account and to_account:
            from_account.transfer(to_account, amount)
        else:
            print("Transfer failed: account not found.")

    def apply_interest_all(self, rate):
        count = 0
        for account in self.bank_accounts.values():
            if isinstance(account, SavingsAccount):
                account.apply_interest(rate)
                count += 1

        print(f"Applied {rate*100:.2f}% interest to {count} account(s)")

    def print_ledger(self):
        for log in self.ledger:
            print(log)

    def save(self, path):
        # to do
        pass
        data = {
            "accounts": [self.bank_accounts],
            "ledger": [self.ledger]
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=4)


class BankAccount:
    def __init__(self, name):
        self.name = name
        self.balance = 0
        self.transaction_history = []

    def log_transaction(self, timestamp, type, amount, balanceAfter, counterparty=None):
        entry = {
            "timestamp": timestamp,
            "type": type,
            "amount": amount,
            "balance_after": balanceAfter,
            "counterparty": counterparty
        }
        self.transaction_history.append(entry)
        bank = getattr(self, "_bank", None)
        if bank is not None:
            self._bank.ledger.append({"account": self.name, **entry})

    def deposit(self, amount):
        if amount <= 0:
            print("Invalid deposit amount.")
            return
        else:
            self.balance += amount
            self.log_transaction(datetime.now(), "deposit", amount, self.balance)

    def depositNoLog(self, amount):
        if amount <= 0:
            print("Invalid deposit amount.")
            return
        else:
            self.balance += amount

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            self.log_transaction(datetime.now(), "withdraw", amount, self.balance)
        else:
            print("Insufficient funds!")

    def withdrawNoLog(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
        else:
            print("Insufficient funds!")

    def get_balance(self):
        return self.balance

    def transfer(self, other_account, amount):
        timestamp = datetime.now()
        if amount > 0 and self.balance >= amount:
            self.withdrawNoLog(amount)
            other_account.depositNoLog(amount)
            print(f"Transferred ${amount} from {self.name} to {other_account.name}.")
            self.log_transaction(timestamp, "transfer_out", amount, self.balance, other_account.name)
            other_account.log_transaction(timestamp, "transfer_in", amount, other_account.balance, self.name)
        else:
            print("Transfer failed: insufficient funds.")

    def print_statement(self, *, start=None, end=None, type=None):
        logs = self.transaction_history
        if start: logs = [l for l in logs if l["timestamp"] >= start]
        if end:   logs = [l for l in logs if l["timestamp"] <= end]
        if type:  logs = [l for l in logs if l["type"] == type]
        for log in logs: print(log, "\n")

    def export_statement(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            headers = ["timestamp", "type", "amount", "balance_after", "counterparty"]
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            for log in self.transaction_history:
                row = [log["timestamp"], log["type"], log["amount"], log["balance_after"], log["counterparty"]]
                writer.writerow(row)
            print(f"Successfully exported {self.name}'s statement as {filename}.")

class CheckingAccount(BankAccount):
    def withdraw(self, amount):
        if amount <= 0:
            print("Insufficient funds!")
            return
        super().withdraw(amount + 1)

class SavingsAccount(BankAccount):
    def apply_interest(self, rate):
        if rate < 0:
            print("Invalid interest rate.")
            return
        interestEarned = self.balance * rate
        self.balance += interestEarned
        self.log_transaction(datetime.now(), "interest", interestEarned, self.balance)


if __name__ == "__main__":
    bank = Bank()
    bank.create_account("Alice", "checking")
    bank.create_account("Bob", "savings")
    alice = bank.get_account("Alice");
    bob = bank.get_account("Bob")
    alice.deposit(100);
    alice.withdraw(20);
    bank.transfer("Alice", "Bob", 50)
    bank.apply_interest_all(0.05)
    # bank.save("bank.json")
    #
    # bank2 = Bank.load("bank.json")
    # assert bank2.get_account("Alice").get_balance() == bank.get_account("Alice").get_balance()
    # assert len(bank2.ledger) == len(bank.ledger)


