# Product Data CLI Tool

A command-line interface (CLI) tool for managing product data.
This tool allows for generating sample products, adding new products, listing existing products, and deleting products.
It can store data in either a JSON file or an SQLite database.

## Setup and Running

This tool is designed to be run as a Python module from the root of the repository.
No external package installations are required beyond a standard Python 3.7+ environment.

### Configuration

**Storage Type:**
The storage backend can be configured via the `PRODUCT_STORAGE_TYPE` environment variable or the `--storage` command-line argument.
- Set `PRODUCT_STORAGE_TYPE=json` or `PRODUCT_STORAGE_TYPE=sqlite`.
- Use `--storage json` or `--storage sqlite` with any command.
- If neither is specified, it defaults to JSON.

The data files (`products.json`, `products.db`) will be created in a `.data_storage/` directory in the project root (this directory is created automatically if it doesn't exist).

### Commands

To run any command, navigate to the root of the repository (the directory containing `product_data_cli/` and `product_api_schema/`).

**General Syntax:**
`python -m product_data_cli.main [common_options] <command> [command_options]`

**Common Options:**
- `--storage {json,sqlite}`: Specify the storage type for this command.

**Available Commands:**

1.  **`generate-sample`**: Generates a few sample products and saves them.
    ```bash
    python -m product_data_cli.main generate-sample
    python -m product_data_cli.main --storage sqlite generate-sample
    ```

2.  **`add`**: Adds a new product.
    ```bash
    python -m product_data_cli.main add "New Amazing Product" -d "This is a great product." -p 49.99
    python -m product_data_cli.main --storage sqlite add "Another Product" -p 100.00
    ```
    - Arguments:
        - `name` (required): Name of the product.
        - `-d, --description` (optional): Description of the product.
        - `-p, --price` (optional): Price of the product (float).

3.  **`list`**: Lists all products or a specific product by UUID.
    ```bash
    python -m product_data_cli.main list
    python -m product_data_cli.main --storage sqlite list
    python -m product_data_cli.main list <product_uuid>
    ```
    - Arguments:
        - `uuid` (optional): UUID of the product to retrieve. If omitted, lists all products.

4.  **`delete`**: Deletes a product by its UUID.
    ```bash
    python -m product_data_cli.main delete <product_uuid>
    python -m product_data_cli.main --storage sqlite delete <product_uuid>
    ```
    - Arguments:
        - `uuid` (required): UUID of the product to delete.

### Example Workflow

1.  **Generate sample data using JSON (default):**
    ```bash
    python -m product_data_cli.main generate-sample
    ```

2.  **List all products (from JSON):**
    ```bash
    python -m product_data_cli.main list
    ```

3.  **Add a new product to SQLite:**
    ```bash
    python -m product_data_cli.main --storage sqlite add "My SQLite Product" -d "First item in DB" -p 1.99
    ```

4.  **List products from SQLite:**
    ```bash
    python -m product_data_cli.main --storage sqlite list
    ```

5.  **Get a specific product by its UUID (copy a UUID from the list output):**
    ```bash
    python -m product_data_cli.main list <paste_uuid_here>
    ```
