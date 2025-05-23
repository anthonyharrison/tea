import requests
import json

BASE_URL = "http://localhost:5000"  # Assuming Flask runs on default port 5000

def print_json_response(response):
    """Helper function to pretty print JSON responses."""
    if response is None:
        print("Error: No response received. The server might be down or the request timed out.")
        return
    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=4))
    except json.JSONDecodeError:
        print("Response content is not valid JSON:")
        print(response.text)

def get_products(base_url, params=None):
    """
    Retrieves a list of products.
    Args:
        base_url (str): The base URL of the API.
        params (dict, optional): Dictionary of query parameters. Defaults to None.
    Returns:
        requests.Response: The response object from the GET request or None on error.
    """
    try:
        response = requests.get(f"{base_url}/products", params=params)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed for GET /products: {e}")
        return None

def get_product_by_uuid(base_url, product_uuid):
    """
    Retrieves a specific product by its UUID.
    Args:
        base_url (str): The base URL of the API.
        product_uuid (str): The UUID of the product to retrieve.
    Returns:
        requests.Response: The response object from the GET request or None on error.
    """
    try:
        response = requests.get(f"{base_url}/product/{product_uuid}")
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed for GET /product/{product_uuid}: {e}")
        return None

def get_component_by_uuid(base_url, component_uuid):
    """Retrieves a specific component by its UUID."""
    try:
        response = requests.get(f"{base_url}/component/{component_uuid}")
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed for GET /component/{component_uuid}: {e}")
        return None

def get_component_releases(base_url, component_uuid, params=None):
    """Retrieves a list of releases for a specific component."""
    try:
        response = requests.get(f"{base_url}/component/{component_uuid}/releases", params=params)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed for GET /component/{component_uuid}/releases: {e}")
        return None

def get_latest_collection_for_release(base_url, release_uuid, params=None):
    """Retrieves the latest collection for a specific release."""
    try:
        response = requests.get(f"{base_url}/release/{release_uuid}/collection", params=params)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed for GET /release/{release_uuid}/collection: {e}")
        return None

def get_collections_for_release(base_url, release_uuid, params=None):
    """Retrieves all collections for a specific release."""
    try:
        response = requests.get(f"{base_url}/release/{release_uuid}/collections", params=params)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed for GET /release/{release_uuid}/collections: {e}")
        return None

def get_collection_version_for_release(base_url, release_uuid, collection_version, params=None):
    """Retrieves a specific version of a collection for a specific release."""
    try:
        response = requests.get(f"{base_url}/release/{release_uuid}/collection/{collection_version}", params=params)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed for GET /release/{release_uuid}/collection/{collection_version}: {e}")
        return None

def get_artifact_by_uuid(base_url, artifact_uuid, params=None):
    """Retrieves a specific artifact by its UUID."""
    try:
        response = requests.get(f"{base_url}/artifact/{artifact_uuid}", params=params)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed for GET /artifact/{artifact_uuid}: {e}")
        return None

if __name__ == '__main__':
    # Example: Test health check
    print("Testing server health...")
    try:
        health_response = requests.get(f"{BASE_URL}/health")
        print_json_response(health_response)
        if health_response is None or health_response.status_code != 200:
            print("Server health check failed. Exiting.")
            import sys
            sys.exit(1)
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {e}")
        print("Please ensure the Flask server is running.")
        import sys
        sys.exit(1)

    print("\nTesting GET /products...")
    products_response = get_products(BASE_URL)
    print_json_response(products_response)

    print("\nTesting GET /products with params (server mock won't filter)...")
    products_params_response = get_products(BASE_URL, params={"idType": "PURL", "idValue": "pkg:generic/mock-product@1.0", "pageOffset": 0, "pageSize": 5})
    print_json_response(products_params_response)

    print("\nTesting GET /product/{uuid} (known UUID)...")
    # This UUID should exist in the mock_products_db in server/app.py
    known_uuid = "09e8c73b-ac45-4475-acac-33e6a7314e6d"
    product_response = get_product_by_uuid(BASE_URL, known_uuid)
    print_json_response(product_response)

    print("\nTesting GET /product/{uuid} (unknown UUID)...")
    unknown_uuid = "00000000-0000-0000-0000-000000000000" 
    product_response_unknown = get_product_by_uuid(BASE_URL, unknown_uuid)
    print_json_response(product_response_unknown)

    # --- Test new functions ---
    print("\n--- Testing Component, Release, Collection, Artifact Endpoints ---")

    # Component Endpoints
    known_component_uuid = "3910e0fd-aff4-48d6-b75f-8bf6b84687f0"
    print(f"\nTesting GET /component/{known_component_uuid} (known UUID)...")
    component_response = get_component_by_uuid(BASE_URL, known_component_uuid)
    print_json_response(component_response)

    print(f"\nTesting GET /component/{unknown_uuid} (unknown UUID)...")
    component_response_unknown = get_component_by_uuid(BASE_URL, unknown_uuid)
    print_json_response(component_response_unknown)

    print(f"\nTesting GET /component/{known_component_uuid}/releases (known component UUID)...")
    component_releases_response = get_component_releases(BASE_URL, known_component_uuid)
    print_json_response(component_releases_response)
    
    print(f"\nTesting GET /component/{unknown_uuid}/releases (unknown component UUID)...")
    component_releases_unknown_response = get_component_releases(BASE_URL, unknown_uuid)
    print_json_response(component_releases_unknown_response)

    # Release Endpoints
    known_release_uuid = "605d0ecb-1057-40e4-9abf-c400b10f0345"
    print(f"\nTesting GET /release/{known_release_uuid}/collection (latest for known release)...")
    latest_collection_response = get_latest_collection_for_release(BASE_URL, known_release_uuid)
    print_json_response(latest_collection_response)

    print(f"\nTesting GET /release/{unknown_uuid}/collection (latest for unknown release)...")
    latest_collection_unknown_response = get_latest_collection_for_release(BASE_URL, unknown_uuid)
    print_json_response(latest_collection_unknown_response)

    print(f"\nTesting GET /release/{known_release_uuid}/collections (all for known release)...")
    collections_response = get_collections_for_release(BASE_URL, known_release_uuid)
    print_json_response(collections_response)

    print(f"\nTesting GET /release/{unknown_uuid}/collections (all for unknown release)...")
    collections_unknown_response = get_collections_for_release(BASE_URL, unknown_uuid)
    print_json_response(collections_unknown_response)

    known_collection_version = 1
    print(f"\nTesting GET /release/{known_release_uuid}/collection/{known_collection_version} (known release, known version)...")
    collection_version_response = get_collection_version_for_release(BASE_URL, known_release_uuid, known_collection_version)
    print_json_response(collection_version_response)
    
    # Test with another version that exists in mock data
    known_collection_version_2 = 2 
    print(f"\nTesting GET /release/{known_release_uuid}/collection/{known_collection_version_2} (known release, another known version)...")
    collection_version_2_response = get_collection_version_for_release(BASE_URL, known_release_uuid, known_collection_version_2)
    print_json_response(collection_version_2_response)

    unknown_collection_version = 999
    print(f"\nTesting GET /release/{known_release_uuid}/collection/{unknown_collection_version} (known release, unknown version)...")
    collection_version_unknown_response = get_collection_version_for_release(BASE_URL, known_release_uuid, unknown_collection_version)
    print_json_response(collection_version_unknown_response)

    # Artifact Endpoint
    # Using an artifact UUID that exists in the mock_artifacts_db in server/app.py
    known_artifact_uuid = "artifact-uuid-1" 
    print(f"\nTesting GET /artifact/{known_artifact_uuid} (known UUID)...")
    artifact_response = get_artifact_by_uuid(BASE_URL, known_artifact_uuid)
    print_json_response(artifact_response)

    print(f"\nTesting GET /artifact/{unknown_uuid} (unknown UUID)...")
    artifact_unknown_response = get_artifact_by_uuid(BASE_URL, unknown_uuid)
    print_json_response(artifact_unknown_response)

    # --- Test new functions ---
    print("\n--- Testing Component, Release, Collection, Artifact Endpoints ---")

    # Component Endpoints
    known_component_uuid = "3910e0fd-aff4-48d6-b75f-8bf6b84687f0"
    print(f"\nTesting GET /component/{known_component_uuid} (known UUID)...")
    component_response = get_component_by_uuid(BASE_URL, known_component_uuid)
    print_json_response(component_response)

    print(f"\nTesting GET /component/{unknown_uuid} (unknown UUID)...")
    component_response_unknown = get_component_by_uuid(BASE_URL, unknown_uuid)
    print_json_response(component_response_unknown)

    print(f"\nTesting GET /component/{known_component_uuid}/releases (known component UUID)...")
    component_releases_response = get_component_releases(BASE_URL, known_component_uuid)
    print_json_response(component_releases_response)
    
    print(f"\nTesting GET /component/{unknown_uuid}/releases (unknown component UUID)...")
    component_releases_unknown_response = get_component_releases(BASE_URL, unknown_uuid)
    print_json_response(component_releases_unknown_response)

    # Release Endpoints
    known_release_uuid = "605d0ecb-1057-40e4-9abf-c400b10f0345"
    print(f"\nTesting GET /release/{known_release_uuid}/collection (latest for known release)...")
    latest_collection_response = get_latest_collection_for_release(BASE_URL, known_release_uuid)
    print_json_response(latest_collection_response)

    print(f"\nTesting GET /release/{unknown_uuid}/collection (latest for unknown release)...")
    latest_collection_unknown_response = get_latest_collection_for_release(BASE_URL, unknown_uuid)
    print_json_response(latest_collection_unknown_response)

    print(f"\nTesting GET /release/{known_release_uuid}/collections (all for known release)...")
    collections_response = get_collections_for_release(BASE_URL, known_release_uuid)
    print_json_response(collections_response)

    print(f"\nTesting GET /release/{unknown_uuid}/collections (all for unknown release)...")
    collections_unknown_response = get_collections_for_release(BASE_URL, unknown_uuid)
    print_json_response(collections_unknown_response)

    known_collection_version = 1
    print(f"\nTesting GET /release/{known_release_uuid}/collection/{known_collection_version} (known release, known version)...")
    collection_version_response = get_collection_version_for_release(BASE_URL, known_release_uuid, known_collection_version)
    print_json_response(collection_version_response)
    
    known_collection_version_2 = 2 # Assuming this version exists for the known_release_uuid
    print(f"\nTesting GET /release/{known_release_uuid}/collection/{known_collection_version_2} (known release, another known version)...")
    collection_version_2_response = get_collection_version_for_release(BASE_URL, known_release_uuid, known_collection_version_2)
    print_json_response(collection_version_2_response)

    unknown_collection_version = 999
    print(f"\nTesting GET /release/{known_release_uuid}/collection/{unknown_collection_version} (known release, unknown version)...")
    collection_version_unknown_response = get_collection_version_for_release(BASE_URL, known_release_uuid, unknown_collection_version)
    print_json_response(collection_version_unknown_response)

    # Artifact Endpoint
    known_artifact_uuid = "artifact-uuid-1" # From mock_artifacts_db
    print(f"\nTesting GET /artifact/{known_artifact_uuid} (known UUID)...")
    artifact_response = get_artifact_by_uuid(BASE_URL, known_artifact_uuid)
    print_json_response(artifact_response)

    print(f"\nTesting GET /artifact/{unknown_uuid} (unknown UUID)...")
    artifact_unknown_response = get_artifact_by_uuid(BASE_URL, unknown_uuid)
    print_json_response(artifact_unknown_response)
