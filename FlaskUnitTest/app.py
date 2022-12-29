from flask import Flask, jsonify, request
import json
from marshmallow import Schema, fields, validate

app = Flask(__name__)

f = open('receipts.json')
data = json.load(f)


class ReceiptSchema(Schema):
    id = fields.Number(required=True)
    store = fields.String(required=True, validate=validate.Length(min=2))
    email = fields.Email(required=True)
    amount = fields.number(required=True)


@app.route('/ping')
def hello_world():  # put application's code here
    return {'pong': True}


@app.route('/receipts/<int:id>')
def get_receipt_by_id(id):
    for receipt in data:
        if receipt['id'] == id:
            return jsonify(receipt)
    return {'message': f'{id} not found'}


@app.route('/receipts/', methods=['POST'])
def add_new_receipt():
    error = ReceiptSchema().validate(data=request.json)
    if error is not None:
        return error, 409


if __name__ == '__main__':
    app.run()
