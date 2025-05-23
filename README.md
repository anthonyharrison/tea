# Transparency Exchange API - Python Implementation

This repository provides a Python-based client and server implementation
for the Transparency Exchange API (TEA).
The server is built using Flask.

## Project Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create and activate a virtual environment:**
    (Recommended)
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install local packages:**
    (This makes the `server` and `client` modules importable as `tea_server` and `tea_client` respectively, and makes their dependencies available.)
    ```bash
    pip install -e ./server
    pip install -e ./client
    ```

## Running the Flask Server

1.  **Ensure your virtual environment is activated.**
2.  **Navigate to the project's root directory.**
3.  **Run the server application:**
    ```bash
    python server/app.py
    ```
    The server will typically start on `http://localhost:5000`. You should see output indicating the server is running.

    ### Configuring the Server Port

    By default, the server runs on port 5000. You can specify a different port by setting the `TEA_SERVER_PORT` environment variable before running the server:

    ```bash
    export TEA_SERVER_PORT=8080  # For Linux/macOS
    # set TEA_SERVER_PORT=8080    # For Windows Command Prompt
    # $env:TEA_SERVER_PORT="8080" # For Windows PowerShell
    python server/app.py
    ```
    The server will then be accessible at `http://localhost:YOUR_PORT` (or `http://0.0.0.0:YOUR_PORT`).

## Using the Client

The client script (`client/client.py`) provides functions to interact with the server API and includes example usage in its `if __name__ == '__main__':` block.

1.  **Ensure the Flask server is running.**
2.  **Open a new terminal and activate the virtual environment.**
3.  **Run the client script:**
    ```bash
    python client/client.py
    ```
    This will execute the example calls defined in the script and print the server's responses. You can modify `client/client.py` to make different API calls.

## Running Unit Tests

Unit tests are located in the `tests/` directory and use the pytest framework.

1.  **Ensure your virtual environment is activated and all dependencies (including local packages) are installed.**
2.  **Navigate to the project's root directory.**
3.  **Run all tests:**
    ```bash
    pytest
    ```
    You can also run tests in specific files or directories:
    ```bash
    pytest tests/test_server.py
    pytest tests/test_client.py
    ```
    Or run specific tests by name using the `-k` flag:
    ```bash
    pytest -k "test_health_check"
    ```
