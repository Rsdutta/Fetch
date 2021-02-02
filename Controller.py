import datetime

from flask import Blueprint, request

from Database import Database
from PayerObject import PayerTransaction
from Service import Service

urls_blueprint = Blueprint('urls', __name__, )
s = Service(Database())


# takes in company, amount, time as json, will return success or failure
@urls_blueprint.route('/add_points', methods=['POST'])
def add_points():
    content = request.json
    date_time_str = content["time"]
    try:
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H')
    except:
        return {"message": "Invalid datetime passed"}, 400
    transaction = PayerTransaction(content["name"], content["amount"], date_time_obj)
    if not transaction.validate():
        return {"message": "ERROR decoding request, ensure types for name, amount and time are correct"}, 400
    else:
        return s.add_points(transaction)


@urls_blueprint.route('/deduct_points', methods=['POST'])
def deduct_points():
    content = request.json
    amount = content["amount"]
    if type(amount) is not int and amount < 0:
        return {"message": "Invalid amount to deduct"}, 400
    return s.deduct_points(amount)


@urls_blueprint.route('/balance', methods=['GET'])
def balance():
    return s.balance()
