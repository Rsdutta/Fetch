import datetime
from collections import defaultdict

from flask import jsonify

from PayerObject import PayerTransaction


class Database:
    def __init__(self):
        self.cumulative_sum = 0
        self.categorized_sum = defaultdict(lambda: 0)
        self.time_series = []

    def add_points(self, transaction: PayerTransaction):
        self.cumulative_sum += transaction.amount
        self.categorized_sum[transaction.name] += transaction.amount
        self.time_series.append(transaction)
        # theres a spot for optimization here, can use a heap
        self.time_series.sort(key=lambda x: x.time)
        return {"message": "Balance Added for " + transaction.name}, 200

    def add_points_negative(self, transaction: PayerTransaction):
        # first check that the given transaction might be possible
        amount_to_deduct = abs(transaction.amount)
        if amount_to_deduct > self.categorized_sum[transaction.name]:
            return {
                       "message": "Error: transaction amount to subtract exceeds existing balance for " + transaction.name}, 400

        counter = 0

        # iterate through time series to see if this subtraction is possible
        for value in self.time_series:
            if value.time > transaction.time:
                return {"message": "Error: Not enough points at time " + transaction.time + " to subtract"}, 400
            if value.name == transaction.name:
                counter += value.amount
            if counter >= amount_to_deduct:
                break

        # need to check if counter is valid because we could have just reached end of array
        if counter < amount_to_deduct:
            return {"message": "Error: Not enough points at time " + transaction.time + " to subtract"}, 400
        # since we havent returned false, we know it's possible
        self.categorized_sum[transaction.name] -= amount_to_deduct
        self.cumulative_sum -= amount_to_deduct
        for i, value in enumerate(self.time_series):
            if value.name == transaction.name:
                if amount_to_deduct >= value.amount:
                    amount_to_deduct -= value.amount
                    self.time_series[i].amount = 0
                else:
                    self.time_series[i].amount -= amount_to_deduct
                    break

        return {"message": "Balance Reduced for " + transaction.name}, 200

    def deduct_points(self, amount: int):
        if amount > self.cumulative_sum:
            return {"message": "Cannot deduct " + str(amount) + " since it exceeds total points available"}, 400

        #we know this is possible since we have enough points
        self.cumulative_sum -= amount
        cache = defaultdict(lambda: 0)

        #same logic as the loop above
        for i, value in enumerate(self.time_series):
            name = value.name
            if amount >= value.amount:
                self.categorized_sum[name] -= value.amount
                amount -= value.amount
                cache[name] -= value.amount
                self.time_series[i].amount = 0
            else:
                self.categorized_sum[name] -= amount
                cache[name] -= amount
                self.time_series[i].amount -= amount
                break

        transactions = []
        time = datetime.datetime.now()
        time.strftime('%Y-%m-%d %H')
        formatted_time = time.strftime('%Y-%m-%d %H')
        for elem in cache:
            temp_payer = PayerTransaction(elem, cache[elem], formatted_time)
            transactions.append(temp_payer)

        return jsonify(message=[e.serialize() for e in transactions]), 200

    def balance(self):
        return {"message": self.categorized_sum}, 200
