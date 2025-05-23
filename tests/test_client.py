import unittest
from unittest.mock import patch, MagicMock
from client import client # Assuming your client code is in client/client.py

class TestClient(unittest.TestCase):

    @patch('client.client.requests.get')
    def test_get_products_success(self, mock_get):
        # Configure the mock response for a successful call
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": [{"name": "Test Product"}]}
        mock_get.return_value = mock_response

        response = client.get_products(base_url="http://fakeapi")
        
        self.assertIsNotNone(response)
        mock_get.assert_called_once_with("http://fakeapi/products", params=None)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['results'][0]['name'], "Test Product")

    @patch('client.client.requests.get')
    def test_get_products_connection_error(self, mock_get):
        # Configure the mock to raise a connection error
        mock_get.side_effect = client.requests.exceptions.ConnectionError

        response = client.get_products(base_url="http://fakeapi")
        
        self.assertIsNone(response) # Assuming function returns None on connection error

    @patch('client.client.requests.get')
    def test_get_product_by_uuid_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"uuid": "test-uuid", "name": "Specific Product"}
        mock_get.return_value = mock_response
        
        test_uuid = "test-uuid"
        response = client.get_product_by_uuid(base_url="http://fakeapi", product_uuid=test_uuid)
        
        self.assertIsNotNone(response)
        mock_get.assert_called_once_with(f"http://fakeapi/product/{test_uuid}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], "Specific Product")

    @patch('client.client.requests.get')
    def test_get_product_by_uuid_not_found(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"error": "Not Found"}
        mock_get.return_value = mock_response
        
        test_uuid = "non-existent-uuid"
        response = client.get_product_by_uuid(base_url="http://fakeapi", product_uuid=test_uuid)
        
        self.assertIsNotNone(response)
        mock_get.assert_called_once_with(f"http://fakeapi/product/{test_uuid}")
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
