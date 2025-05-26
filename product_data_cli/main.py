import argparse
import sys
import os
from .data_models import Product
from .storage import (
    save_products_json, load_products_json,
    init_db, save_product_db, load_all_products_db, load_product_by_uuid_db, delete_product_db,
    JSON_STORAGE_PATH, DB_STORAGE_PATH
)

# Determine storage type (this could be enhanced with config files or env vars)
DEFAULT_STORAGE_TYPE = "json" # or "sqlite"

def get_storage_type(args):
    if hasattr(args, 'storage') and args.storage:
        return args.storage
    return os.environ.get("PRODUCT_STORAGE_TYPE", DEFAULT_STORAGE_TYPE).lower()

# --- Handler functions for CLI commands ---

def handle_generate_sample(args):
    storage_type = get_storage_type(args)
    print(f"Generating sample data for '{storage_type}' storage...")

    sample_products = [
        Product(name="Organic Green Tea", description="A refreshing and healthy green tea.", price=12.99),
        Product(name="Artisan Coffee Beans", description="Dark roast, single origin.", price=18.50),
        Product(name="Stainless Steel Water Bottle", description="1L, keeps drinks cold for 24h.", price=25.00)
    ]

    if storage_type == "json":
        # For JSON, we typically save the whole list
        existing_products = load_products_json()
        # Avoid duplicates if run multiple times (simple check by name)
        existing_names = {p.name for p in existing_products}
        new_samples = [p for p in sample_products if p.name not in existing_names]
        all_products_to_save = existing_products + new_samples
        save_products_json(all_products_to_save)
        print(f"Added {len(new_samples)} new sample products to '{JSON_STORAGE_PATH}'. Total: {len(all_products_to_save)}.")
    elif storage_type == "sqlite":
        init_db() # Ensure DB and table exist
        count = 0
        for product in sample_products:
            # save_product_db handles insert/update, so it won't duplicate by UUID
            # but we might want to avoid re-inserting if run multiple times based on other criteria
            # For simplicity here, we just save. A real app might check existence first.
            existing = load_product_by_uuid_db(product.uuid) # Assumes default UUIDs are stable if not re-gened
            if not existing: # Only add if UUID isn't there (less likely for default UUIDs)
                             # A better check might be by name if UUIDs are random.
                save_product_db(product)
                count +=1
        print(f"Saved/updated {len(sample_products)} sample products in SQLite database '{DB_STORAGE_PATH}'. {count} were new.")
    else:
        print(f"Error: Unknown storage type '{storage_type}'. Use 'json' or 'sqlite'.", file=sys.stderr)
        sys.exit(1)

def handle_add_product(args):
    storage_type = get_storage_type(args)
    print(f"Adding new product to '{storage_type}' storage...")
    try:
        price = float(args.price) if args.price is not None else 0.0
        product = Product(name=args.name, description=args.description or "", price=price)
    except ValueError as e:
        print(f"Error creating product: {e}", file=sys.stderr)
        sys.exit(1)

    if storage_type == "json":
        products = load_products_json()
        products.append(product)
        save_products_json(products)
        print(f"Product '{product.name}' added to '{JSON_STORAGE_PATH}'.")
    elif storage_type == "sqlite":
        init_db()
        save_product_db(product)
        print(f"Product '{product.name}' added to SQLite database '{DB_STORAGE_PATH}'.")
    else:
        print(f"Error: Unknown storage type '{storage_type}'. Use 'json' or 'sqlite'.", file=sys.stderr)
        sys.exit(1)
    print(f"UUID: {product.uuid}, Name: {product.name}, Price: {product.price:.2f}")


def handle_list_products(args):
    storage_type = get_storage_type(args)
    print(f"Listing products from '{storage_type}' storage ({'all' if not args.uuid else args.uuid}):")
    
    products: List[Product] = []
    if storage_type == "json":
        all_prods = load_products_json()
        if args.uuid:
            products = [p for p in all_prods if p.uuid == args.uuid]
        else:
            products = all_prods
    elif storage_type == "sqlite":
        init_db()
        if args.uuid:
            product = load_product_by_uuid_db(args.uuid)
            if product:
                products = [product]
        else:
            products = load_all_products_db()
    else:
        print(f"Error: Unknown storage type '{storage_type}'. Use 'json' or 'sqlite'.", file=sys.stderr)
        sys.exit(1)

    if not products:
        if args.uuid:
            print(f"Product with UUID '{args.uuid}' not found.")
        else:
            print("No products found.")
        return

    for product in products:
        print(f"  UUID: {product.uuid}")
        print(f"  Name: {product.name}")
        if product.description:
            print(f"  Description: {product.description}")
        print(f"  Price: ${product.price:.2f}")
        print(f"  Created: {product.created_at.isoformat()}")
        print(f"  Updated: {product.updated_at.isoformat()}")
        print("-" * 20)

def handle_delete_product(args):
    storage_type = get_storage_type(args)
    print(f"Deleting product UUID '{args.uuid}' from '{storage_type}' storage...")

    deleted = False
    if storage_type == "json":
        products = load_products_json()
        original_count = len(products)
        products_to_keep = [p for p in products if p.uuid != args.uuid]
        if len(products_to_keep) < original_count:
            save_products_json(products_to_keep)
            deleted = True
    elif storage_type == "sqlite":
        init_db()
        deleted = delete_product_db(args.uuid)
    else:
        print(f"Error: Unknown storage type '{storage_type}'. Use 'json' or 'sqlite'.", file=sys.stderr)
        sys.exit(1)

    if deleted:
        print(f"Product with UUID '{args.uuid}' deleted successfully.")
    else:
        print(f"Product with UUID '{args.uuid}' not found or could not be deleted.")


def main():
    parser = argparse.ArgumentParser(description="Product Data Management CLI Tool")
    parser.add_argument('--storage', choices=['json', 'sqlite'],
                        help="Storage type to use (json or sqlite). Overrides PRODUCT_STORAGE_TYPE env var.")

    subparsers = parser.add_subparsers(title="Commands", dest="command", required=True)

    # Generate Sample Data command
    parser_generate = subparsers.add_parser('generate-sample', help="Generate and store sample products.")
    parser_generate.set_defaults(func=handle_generate_sample)

    # Add Product command
    parser_add = subparsers.add_parser('add', help="Add a new product.")
    parser_add.add_argument('name', help="Name of the product.")
    parser_add.add_argument('-d', '--description', help="Description of the product.")
    parser_add.add_argument('-p', '--price', type=float, help="Price of the product.")
    parser_add.set_defaults(func=handle_add_product)

    # List Products / Get Product command
    parser_list = subparsers.add_parser('list', help="List all products or a specific product by UUID.")
    parser_list.add_argument('uuid', nargs='?', default=None, help="UUID of the product to retrieve (optional).")
    parser_list.set_defaults(func=handle_list_products)
    
    # Delete Product command
    parser_delete = subparsers.add_parser('delete', help="Delete a product by UUID.")
    parser_delete.add_argument('uuid', help="UUID of the product to delete.")
    parser_delete.set_defaults(func=handle_delete_product)

    if len(sys.argv) == 1: # No command provided
        # If PRODUCT_STORAGE_TYPE is not set, init_db for sqlite won't run by default.
        # We can choose to initialize default storage here if needed, e.g.
        # if get_storage_type(parser.parse_args([])) == "sqlite": # parse empty to get default storage
        #    init_db()
        # print("Defaulting SQLite DB initialized (if applicable).")
        parser.print_help(sys.stderr)
        sys.exit(1)
        
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    # This allows running the CLI directly, e.g. python -m product_data_cli.main list
    # For it to find modules in the current package when run with `python product_data_cli/main.py`,
    # the `product_data_cli` parent directory should be in PYTHONPATH, or use `python -m product_data_cli.main`
    main()
