class Account:
    """A safe bank account using private attributes and controlled access."""

    def __init__(self, account_holder, pin, balance=0):
        self.__account_holder = account_holder
        self.__pin = self.__validate_pin(pin)
        self.__balance = balance

    def __validate_pin(self, pin):
        pin = str(pin)
        if len(pin) != 4 or not pin.isdigit():
            raise ValueError("PIN must be exactly 4 digits.")
        return pin

    @property
    def account_holder(self):
        return self.__account_holder

    @account_holder.setter
    def account_holder(self, new_name):
        if not new_name or not new_name.strip():
            raise ValueError("Account holder name cannot be empty.")
        self.__account_holder = new_name.strip()

    @property
    def pin(self):
        return self.__pin

    @pin.setter
    def pin(self, new_pin):
        self.__pin = self.__validate_pin(new_pin)

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, amount):
        if amount < 0:
            raise ValueError("Balance cannot be negative.")
        self.__balance = amount

    def check_pin(self, entered_pin):
        return str(entered_pin) == self.__pin

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.__balance += amount
        return f"Deposited ${amount}. New balance: ${self.__balance}"

    def withdraw(self, amount, entered_pin):
        if not self.check_pin(entered_pin):
            return "PIN is incorrect. Withdrawal denied."
        if amount > self.__balance:
            return "Insufficient funds."
        self.__balance -= amount
        return f"Withdrew ${amount}. Remaining balance: ${self.__balance}"

    def update_pin(self, old_pin, new_pin):
        if not self.check_pin(old_pin):
            raise PermissionError("Old PIN is incorrect.")
        self.pin = new_pin
        return "PIN updated successfully."

    def __str__(self):
        return (
            f"Account Holder: {self.__account_holder}\n"
            f"PIN: ****\n"
            f"Balance: ${self.__balance}"
        )


# Demo
account = Account("Aisha Khan", 1234, 2500)
print("Original account:")
print(account)

print("\nPrivate attribute access outside class:")
try:
    print(account.__account_holder)
except AttributeError as error:
    print("Blocked:", error)

print("\nPIN check:")
print(account.check_pin(1234))

print("\nUpdate PIN using setter method:")
account.pin = 4321
print(account)

print("\nUpdate account holder using setter method:")
account.account_holder = "Aisha Rahman"
print(account)
