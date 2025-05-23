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

## Running the Flask Server

1.  **Ensure your virtual environment is activated.**
2.  **Navigate to the project's root directory.**
3.  **Run the server application:**
    ```bash
    python server/app.py
    ```
    The server will typically start on `http://localhost:5000`. You should see output indicating the server is running.

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

Unit tests are located in the `tests/` directory.

1.  **Ensure your virtual environment is activated and dependencies are installed.**
2.  **Navigate to the project's root directory.**
3.  **Run all tests:**
    ```bash
    python -m unittest discover -s tests
    ```
    Alternatively, you can run specific test files:
    ```bash
    python -m unittest tests/test_server.py
    python -m unittest tests/test_client.py
    ```
