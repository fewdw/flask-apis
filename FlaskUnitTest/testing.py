import json
import unittest

from flask import jsonify

from app import app


class BaseCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()


class TestPing(BaseCase):
    def test_ping_pong(self):
        response = self.app.get('ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['pong'], True)


class TestReceipts(BaseCase):
    def test_get_receipt_by_id_existing(self):
        response = self.app.get('/receipts/1')
        receipt_1 = {"id": 1, "store": "Mydo", "email": "dradford0@oaic.gov.au", "amount": 62}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, receipt_1)

    def test_add_new_receipt(self):
        wrong_receipt_data = json.dumps({'amount': 23, 'email': 'asad@ds.com', 'store': 'a'})
        response = self.app.post('receipts', headers={"Content-Type": "application/json"}, data=wrong_receipt_data)
        self.assertEqual(response.status_code, 409)


if __name__ == '__main__':
    unittest.main()
