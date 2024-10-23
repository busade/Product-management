import unittest
from flask import Flask
from API import create_app
from ..utils import db
from ..model import Products

class Test_Product(unittest.TestCase):

    def setUp(self):
        self.app = create_app('test')  # Pass in 'testing' config if you have it
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create all tables
        db.create_all()
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_product_success(self):
        product_data = {
            "name": "Test Product",
            "info": "Test product info",
            "quantity": 100
        }
        response = self.client.post('/product', json=product_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Test Product", response.get_json()['name'])




    def test_delete_product_success(self):
        # Create a product first
        new_product = Products(name="Test Product", info="Test Info", quantity=10)
        db.session.add(new_product)
        db.session.commit()

        # print(new_product)
        # response = self.app.test_client().delete(f'/product/{new_product.id}')
        # self.assertEqual(response.status_code, 202)

    def test_delete_product_not_found(self):
        response = self.app.test_client().delete('/product/9999')  
        self.assertEqual(response.status_code, 404)
        # self.assertIn("Product with ID 9999 does not exist", response.get_json()['message'])
    

    def test_retrieve(self):
        respone = self.client.get('product')
        self.assertEqual(respone.status_code,200)
    

if __name__ == "__main__":
    unittest.main()