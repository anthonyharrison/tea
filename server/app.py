from flask import Flask, jsonify, request
from datetime import datetime, timezone

app = Flask(__name__)

# Mock data store
mock_products_db = {
    "09e8c73b-ac45-4475-acac-33e6a7314e6d": {
        "uuid": "09e8c73b-ac45-4475-acac-33e6a7314e6d",
        "name": "Mock Product Name",
        "identifiers": [
            {"idType": "PURL", "idValue": "pkg:generic/mock-product@1.0"}
        ],
        "components": [
            "3910e0fd-aff4-48d6-b75f-8bf6b84687f0"
        ]
    },
    "another-uuid-placeholder": { # Add another product for the paginated list
        "uuid": "another-uuid-placeholder",
        "name": "Another Mock Product",
        "identifiers": [
            {"idType": "CPE", "idValue": "cpe:/a:mock_vendor:another_product:2.3"}
        ],
        "components": [
            "some-component-uuid-1",
            "some-component-uuid-2"
        ]
    }
}

mock_components_db = {
    "3910e0fd-aff4-48d6-b75f-8bf6b84687f0": {
        "uuid": "3910e0fd-aff4-48d6-b75f-8bf6b84687f0",
        "name": "Mock Component Name",
        "identifiers": [{"idType": "PURL", "idValue": "pkg:generic/mock-component@1.0"}]
    },
    "some-component-uuid-1": {
        "uuid": "some-component-uuid-1",
        "name": "Another Component",
        "identifiers": [{"idType": "PURL", "idValue": "pkg:generic/another-component@0.5"}]
    }
}

mock_releases_db = {
    "605d0ecb-1057-40e4-9abf-c400b10f0345": {
        "uuid": "605d0ecb-1057-40e4-9abf-c400b10f0345",
        "version": "1.0.0",
        "releaseDate": "2024-07-29T10:00:00Z",
        "component_uuid": "3910e0fd-aff4-48d6-b75f-8bf6b84687f0" # Link to component
    },
    "release-for-another-component": {
        "uuid": "release-for-another-component",
        "version": "0.5.1",
        "releaseDate": "2024-07-28T12:00:00Z",
        "component_uuid": "some-component-uuid-1"
    }
}

mock_collections_db = {
    "collection-for-release-605d": {
        "uuid": "collection-for-release-605d",
        "version": 1, # Integer version
        "date": "2024-07-29T11:00:00Z",
        "artifacts": ["artifact-uuid-1", "artifact-uuid-2"],
        "release_uuid": "605d0ecb-1057-40e4-9abf-c400b10f0345" # Link to release
    },
     "collection-v2-for-release-605d": {
        "uuid": "collection-v2-for-release-605d",
        "version": 2, # Integer version
        "date": "2024-07-30T11:00:00Z",
        "artifacts": ["artifact-uuid-3"],
        "release_uuid": "605d0ecb-1057-40e4-9abf-c400b10f0345" # Link to release
    }
}

mock_artifacts_db = {
    "artifact-uuid-1": {
        "uuid": "artifact-uuid-1",
        "name": "component-manifest.json",
        "type": "cyclonedx_json", # Example type
        "formats": [{"format": "json", "signature": "abc123signature"}]
    },
    "artifact-uuid-2": {
        "uuid": "artifact-uuid-2",
        "name": "readme.md",
        "type": "documentation",
        "formats": [{"format": "markdown", "signature": "def456signature"}]
    },
    "artifact-uuid-3": {
        "uuid": "artifact-uuid-3",
        "name": "updated-manifest.json",
        "type": "cyclonedx_json",
        "formats": [{"format": "json", "signature": "ghi789signature"}]
    }
}

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "UP"}), 200

@app.route('/product/<uuid:uuid>', methods=['GET'])
def get_product_by_uuid(uuid):
    product = mock_products_db.get(str(uuid))
    if product:
        return jsonify(product), 200
    else:
        return jsonify({"error": "Product not found"}), 404

@app.route('/products', methods=['GET'])
def get_products():
    # For simplicity, pagination parameters (pageStartIndex, pageSize) are ignored for now
    # and all mock products are returned.
    # A real implementation would use these parameters to slice the data.
    
    all_products = list(mock_products_db.values())
    
    response_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pageStartIndex": 0, # Assuming default for now
        "pageSize": len(all_products), # Assuming all results fit in one page for now
        "totalResults": len(all_products),
        "results": all_products
    }
    return jsonify(response_data), 200

@app.route('/component/<uuid:uuid>', methods=['GET'])
def get_component_by_uuid(uuid):
    component = mock_components_db.get(str(uuid))
    if component:
        return jsonify(component), 200
    else:
        return jsonify({"error": "Component not found"}), 404

@app.route('/component/<uuid:uuid>/releases', methods=['GET'])
def get_component_releases(uuid):
    # Check if component exists
    if str(uuid) not in mock_components_db:
        return jsonify({"error": "Component not found"}), 404
    
    releases = [
        release for release in mock_releases_db.values() 
        if release["component_uuid"] == str(uuid)
    ]
    
    if releases:
        # Return only a subset of fields for the list view, as per typical API design
        # For now, returning full objects for simplicity in mock
        return jsonify(releases), 200
    else:
        # It's valid for a component to have no releases yet
        return jsonify([]), 200

@app.route('/release/<uuid:uuid>/collection', methods=['GET'])
def get_latest_collection_for_release(uuid):
    # Check if release exists
    if str(uuid) not in mock_releases_db:
        return jsonify({"error": "Release not found"}), 404

    release_collections = [
        coll for coll in mock_collections_db.values() 
        if coll["release_uuid"] == str(uuid)
    ]
    
    if not release_collections:
        return jsonify({"error": "No collections found for this release"}), 404
        
    # Sort by date or version to get the latest. Assuming 'version' is the primary sort key.
    latest_collection = sorted(release_collections, key=lambda x: x["version"], reverse=True)[0]
    return jsonify(latest_collection), 200

@app.route('/release/<uuid:uuid>/collections', methods=['GET'])
def get_collections_for_release(uuid):
    # Check if release exists
    if str(uuid) not in mock_releases_db:
        return jsonify({"error": "Release not found"}), 404
        
    release_collections = [
        coll for coll in mock_collections_db.values() 
        if coll["release_uuid"] == str(uuid)
    ]
    
    if release_collections:
        return jsonify(release_collections), 200
    else:
        return jsonify([]), 200 # No collections for this release yet

@app.route('/release/<uuid:uuid>/collection/<int:version>', methods=['GET'])
def get_collection_by_version_for_release(uuid, version):
    # Check if release exists
    if str(uuid) not in mock_releases_db:
        return jsonify({"error": "Release not found"}), 404
        
    collection = next((
        coll for coll in mock_collections_db.values() 
        if coll["release_uuid"] == str(uuid) and coll["version"] == version
    ), None)
    
    if collection:
        return jsonify(collection), 200
    else:
        return jsonify({"error": "Collection with specified version not found for this release"}), 404

@app.route('/artifact/<uuid:uuid>', methods=['GET'])
def get_artifact_by_uuid(uuid):
    artifact = mock_artifacts_db.get(str(uuid))
    if artifact:
        return jsonify(artifact), 200
    else:
        return jsonify({"error": "Artifact not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
