from PayerObject import PayerTransaction


class Service:
    def __init__(self, database):
        self.db = database;

    def add_points(self, transaction: PayerTransaction):
        # first check if negative
        if transaction.amount < 0:
            return self.add_points_negative(transaction)
        else:
            return self.db.add_points(transaction)

    def add_points_negative(self, transaction: PayerTransaction):
        return self.db.add_points_negative(transaction)

    def deduct_points(self, amount):
        return self.db.deduct_points(amount)

    def balance(self):
        return self.db.balance()
