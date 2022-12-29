from flask import Flask, jsonify, request
import json

app = Flask(__name__)

f = open('receipts.json')
# returns JSON object of the data
# in this case it will be a list of dictionaries
data = json.load(f)


def dump_data():
    with open('receipts.json', 'w') as outfile:
        json.dump(data, outfile)


@app.route('/ping')
def ping():  # put application's code here
    var = {'Pong': True}
    return jsonify(var)


@app.route('/receipts/<id>')
def get_receipts_by_id(id):
    for receipt in data:
        if receipt['id'] == int(id):
            return receipt
    return f'{id} not found', 404


@app.route('/receipts/', methods=['POST'])
def post_new_receipt():
    store = request.json.get('store')
    email = request.json.get('email')
    amount = request.json.get('amount')

    for key in [store, email, amount]:
        if key is None:
            return 404

    max = 0
    for receipt in data:
        if int(receipt['id']) > max:
            max = int(receipt['id'])
    max + 1

    receipt = {'id': max, 'store': store, 'email': email, 'amount': amount}
    return jsonify(receipt)

#http://127.0.0.1:5000/receipts/?max_amount=65&top=2
@app.route('/receipts/', methods=['GET'])
def get_min_and_max():
    max_amount = int(request.args.get('max_amount'))
    top = int(request.args.get('top'))
    for key in [max_amount,top]:
        if key != 0:
            count = 0
            list = []
            for receipt in data:
                if receipt['amount'] < max_amount and top != count:
                    list.append(receipt)
                    count = count + 1
            return jsonify(list)


@app.route('/maxid')
def get_max_id():
    max = 0
    for receipt in data:
        if int(receipt['id']) > max:
            max = int(receipt['id'])
            print(max)
    max = max + 1
    return str(max)


if __name__ == '__main__':
    app.run()
