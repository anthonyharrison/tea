import json # Not strictly needed if using response.json for all cases
# The app import is not strictly needed here if conftest.py provides the app fixture
# and client fixture is used, but can be kept for clarity or direct app access if needed.
# from tea_server.app import app

# The 'client' fixture is provided by pytest-flask, using the 'app' fixture from conftest.py.

def test_health_check(client): # client is provided by pytest-flask
    response = client.get('/health')
    assert response.status_code == 200
    # response.json is a helper from Flask's test client / pytest-flask
    assert response.json['status'] == 'UP'

def test_get_products(client):
    response = client.get('/products')
    assert response.status_code == 200
    data = response.json
    assert 'results' in data
    assert isinstance(data['results'], list)
    if data['results']: # If there are products, check the first one's structure
        # Assuming the mock data includes these keys for the first product
        assert 'uuid' in data['results'][0]
        assert 'name' in data['results'][0]

def test_get_product_by_known_uuid(client):
    # This UUID should exist in your server's mock_products_db
    known_uuid = "09e8c73b-ac45-4475-acac-33e6a7314e6d"
    response = client.get(f'/product/{known_uuid}')
    assert response.status_code == 200
    data = response.json
    assert data['uuid'] == known_uuid
    assert 'name' in data

def test_get_product_by_unknown_uuid(client):
    unknown_uuid = "00000000-0000-0000-0000-000000000000"
    response = client.get(f'/product/{unknown_uuid}')
    assert response.status_code == 404
    data = response.json
    assert 'error' in data # Assuming your 404 response includes an error message
