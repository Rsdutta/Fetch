import datetime


class PayerTransaction:
    def __init__(self, name: str, amount: int, time: datetime):
        self.name = name
        self.amount = amount
        self.time = time

    def validate(self):
        return not (self.name is None or self.amount is None or self.time is None)

    def serialize(self):
        return {
            'name': self.name,
            'amount': self.amount,
            'time': self.time,
        }
