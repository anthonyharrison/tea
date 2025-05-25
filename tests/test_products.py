# tests/test_products.py
from client import client as tea_client_module # New import: from /app/client import client.py
import requests # For requests.exceptions.ConnectionError

# pytest-mock provides the 'mocker' fixture automatically

def test_get_products_success(mocker):
    # Configure the mock response
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"results": [{"name": "Test Product"}]}
    
    # Patch requests.get within the client.client module
    mock_get = mocker.patch('client.client.requests.get', return_value=mock_response)

    response = tea_client_module.get_products(base_url="http://fakeapi")
    
    assert response is not None
    mock_get.assert_called_once_with("http://fakeapi/products", params=None)
    assert response.status_code == 200
    assert response.json()['results'][0]['name'] == "Test Product"

def test_get_products_connection_error(mocker):
    # Configure the mock to raise a connection error
    mock_get = mocker.patch('client.client.requests.get', side_effect=requests.exceptions.ConnectionError)

    response = tea_client_module.get_products(base_url="http://fakeapi")
    
    assert response is None # Assuming function returns None on connection error

def test_get_product_by_uuid_success(mocker):
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"uuid": "test-uuid", "name": "Specific Product"}
    
    mock_get = mocker.patch('client.client.requests.get', return_value=mock_response)
            
    test_uuid = "test-uuid"
    response = tea_client_module.get_product_by_uuid(base_url="http://fakeapi", product_uuid=test_uuid)
    
    assert response is not None
    mock_get.assert_called_once_with(f"http://fakeapi/product/{test_uuid}")
    assert response.status_code == 200
    assert response.json()['name'] == "Specific Product"

def test_get_product_by_uuid_not_found(mocker):
    mock_response = mocker.MagicMock()
    mock_response.status_code = 404
    mock_response.json.return_value = {"error": "Not Found"}

    mock_get = mocker.patch('client.client.requests.get', return_value=mock_response)
            
    test_uuid = "non-existent-uuid"
    response = tea_client_module.get_product_by_uuid(base_url="http://fakeapi", product_uuid=test_uuid)
    
    assert response is not None
    mock_get.assert_called_once_with(f"http://fakeapi/product/{test_uuid}")
    assert response.status_code == 404
    assert response.json()['error'] == "Not Found" # Check error message
