class User:
    def __init__(self, username, name, age, contact, password):
        self.username = username
        self.name = name
        self.age = age
        self.contact = contact
        self.password = password
        self.balance = 0.0
        self.transactions = []  # Store transaction history


class BankSystem:
    def __init__(self):
        self.users = {}
        self.current_user = None

    def register_user(self, username, name, age, contact, password):
        if username in self.users:
            return "❌ Username already exists."
        self.users[username] = User(username, name, age, contact, password)
        return "✅ Account created successfully!"

    def login_user(self, username, password):
        user = self.users.get(username)
        if not user or user.password != password:
            return "❌ Invalid username or password."
        self.current_user = user
        return f"✅ Welcome, {user.name}!"

    def logout_user(self):
        self.current_user = None

    def get_current_user(self):
        return self.current_user

    def deposit(self, amount):
        if self.current_user:
            self.current_user.balance += amount
            self.current_user.transactions.append(f"➕ Deposited ₹{amount:.2f}")
            return f"✅ Deposited ₹{amount:.2f} successfully!"
        return "❌ No user logged in."

    def withdraw(self, amount):
        if self.current_user:
            if self.current_user.balance >= amount:
                self.current_user.balance -= amount
                self.current_user.transactions.append(f"➖ Withdrew ₹{amount:.2f}")
                return f"✅ Withdrawn ₹{amount:.2f} successfully!"
            return "❌ Insufficient balance."
        return "❌ No user logged in."
