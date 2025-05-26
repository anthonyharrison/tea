import json
import sqlite3
import os
from typing import List, Optional, Dict, Any
from .data_models import Product # Assuming data_models.py is in the same directory

# Define storage paths
STORAGE_DIR = os.path.join(os.path.dirname(__file__), '..', '.data_storage') # Store data outside the module
JSON_STORAGE_PATH = os.path.join(STORAGE_DIR, 'products.json')
DB_STORAGE_PATH = os.path.join(STORAGE_DIR, 'products.db')

def _ensure_storage_dir_exists():
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)

# --- JSON File Storage ---
def save_products_json(products: List[Product], filepath: str = JSON_STORAGE_PATH) -> None:
    _ensure_storage_dir_exists()
    data_to_save = [product.to_dict() for product in products]
    with open(filepath, 'w') as f:
        json.dump(data_to_save, f, indent=4)

def load_products_json(filepath: str = JSON_STORAGE_PATH) -> List[Product]:
    _ensure_storage_dir_exists()
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            return [Product.from_dict(p_data) for p_data in data]
    except json.JSONDecodeError:
        # Handle empty or corrupted file
        return []

# --- SQLite Database Storage ---
def _get_db_connection(db_path: str = DB_STORAGE_PATH) -> sqlite3.Connection:
    _ensure_storage_dir_exists()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row # Access columns by name
    return conn

def init_db(db_path: str = DB_STORAGE_PATH) -> None:
    conn = _get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        uuid TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        price REAL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def save_product_db(product: Product, db_path: str = DB_STORAGE_PATH) -> None:
    init_db(db_path) # Ensure table exists
    conn = _get_db_connection(db_path)
    cursor = conn.cursor()
    # Check if product exists for update or insert
    cursor.execute("SELECT uuid FROM products WHERE uuid = ?", (product.uuid,))
    existing_product = cursor.fetchone()

    product_dict = product.to_dict()
    
    # Need datetime for updated_at if it's a new insert or explicit update
    from datetime import datetime, timezone

    if existing_product:
        # Update existing product
        product_dict['updated_at'] = datetime.now(timezone.utc).isoformat() # Update timestamp
        cursor.execute('''
        UPDATE products SET name = ?, description = ?, price = ?, updated_at = ?
        WHERE uuid = ?
        ''', (product_dict['name'], product_dict['description'], product_dict['price'],
              product_dict['updated_at'], product.uuid))
    else:
        # Insert new product - ensure created_at and updated_at are current ISO strings if not set by Product
        if not isinstance(product_dict['created_at'], str):
             product_dict['created_at'] = datetime.now(timezone.utc).isoformat()
        if not isinstance(product_dict['updated_at'], str):
             product_dict['updated_at'] = datetime.now(timezone.utc).isoformat()

        cursor.execute('''
        INSERT INTO products (uuid, name, description, price, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (product.uuid, product_dict['name'], product_dict['description'], product_dict['price'],
              product_dict['created_at'], product_dict['updated_at']))
    conn.commit()
    conn.close()

def load_all_products_db(db_path: str = DB_STORAGE_PATH) -> List[Product]:
    init_db(db_path) # Ensure table exists
    conn = _get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    conn.close()
    return [Product.from_dict(dict(row)) for row in rows]

def load_product_by_uuid_db(product_uuid: str, db_path: str = DB_STORAGE_PATH) -> Optional[Product]:
    init_db(db_path) # Ensure table exists
    conn = _get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE uuid = ?", (product_uuid,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Product.from_dict(dict(row))
    return None

def delete_product_db(product_uuid: str, db_path: str = DB_STORAGE_PATH) -> bool:
    init_db(db_path) # Ensure table exists
    conn = _get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE uuid = ?", (product_uuid,))
    conn.commit()
    deleted_rows = cursor.rowcount
    conn.close()
    return deleted_rows > 0

# --- Unified Storage Interface (Optional - for CLI to use) ---
# This part might be better in main.py or a dedicated cli_logic.py
# For now, just providing the core DB and JSON functions.

if __name__ == '__main__':
    # Basic Test for storage functions
    from datetime import datetime, timezone # Ensure datetime is available for tests
    print("Testing JSON storage...")
    _ensure_storage_dir_exists() # Ensure .data_storage exists for testing
    # Clean up old JSON file if it exists
    if os.path.exists(JSON_STORAGE_PATH):
        os.remove(JSON_STORAGE_PATH)

    sample_product1 = Product(name="JSON Test Product 1", price=10.99)
    sample_product2 = Product(name="JSON Test Product 2", description="Desc for P2", price=19.99)
    
    save_products_json([sample_product1, sample_product2])
    loaded_json_products = load_products_json()
    print(f"Loaded {len(loaded_json_products)} products from JSON.")
    for p in loaded_json_products:
        print(f"- {p.name} (UUID: {p.uuid})")
    assert len(loaded_json_products) == 2

    print("\nTesting SQLite storage...")
    # Clean up old DB file if it exists for a fresh test
    if os.path.exists(DB_STORAGE_PATH):
        os.remove(DB_STORAGE_PATH)
    
    init_db() # Create table
    db_product1 = Product(name="DB Test Product 1", price=100.50)
    db_product2 = Product(name="DB Test Product 2", description="SQLite item", price=75.25)

    save_product_db(db_product1)
    save_product_db(db_product2)

    loaded_db_products = load_all_products_db()
    print(f"Loaded {len(loaded_db_products)} products from SQLite.")
    for p in loaded_db_products:
        print(f"- {p.name} (UUID: {p.uuid}, Price: {p.price})")
    assert len(loaded_db_products) == 2

    retrieved_p1 = load_product_by_uuid_db(db_product1.uuid)
    print(f"Retrieved product by UUID: {retrieved_p1.name if retrieved_p1 else 'Not Found'}")
    assert retrieved_p1 is not None and retrieved_p1.uuid == db_product1.uuid

    # Test update
    if retrieved_p1:
        retrieved_p1.name = "Updated DB Product 1 Name"
        retrieved_p1.price = 99.99
        # The `save_product_db` function now handles setting updated_at
        save_product_db(retrieved_p1) 
        
        updated_p1 = load_product_by_uuid_db(db_product1.uuid)
        print(f"After update: Name='{updated_p1.name}', Price='{updated_p1.price}'")
        assert updated_p1.name == "Updated DB Product 1 Name"
        assert updated_p1.price == 99.99


    delete_product_db(db_product1.uuid)
    deleted_p1 = load_product_by_uuid_db(db_product1.uuid)
    print(f"After delete, retrieved product by UUID: {deleted_p1.name if deleted_p1 else 'Not Found (Correct!)'}")
    assert deleted_p1 is None
    
    remaining_products = load_all_products_db()
    print(f"Remaining products after delete: {len(remaining_products)}")
    assert len(remaining_products) == 1

    print("\nStorage tests completed.")
