import unittest
import json
from server.app import app # Assuming your Flask app instance is named 'app' in server/app.py

class TestServer(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_health_check(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['status'], 'UP')

    def test_get_products(self):
        response = self.app.get('/products')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('results', data)
        self.assertIsInstance(data['results'], list)
        if data['results']: # If there are products, check the first one's structure
            self.assertIn('uuid', data['results'][0])
            self.assertIn('name', data['results'][0])

    def test_get_product_by_known_uuid(self):
        # This UUID should exist in your server's mock_products_db
        known_uuid = "09e8c73b-ac45-4475-acac-33e6a7314e6d"
        response = self.app.get(f'/product/{known_uuid}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['uuid'], known_uuid)
        self.assertIn('name', data)

    def test_get_product_by_unknown_uuid(self):
        unknown_uuid = "00000000-0000-0000-0000-000000000000"
        response = self.app.get(f'/product/{unknown_uuid}')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('error', data) # Assuming your 404 response includes an error message

if __name__ == '__main__':
    unittest.main()
