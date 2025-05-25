import pytest
# from tea_server.app import app as flask_app # Original import commented out or replaced
from server.app import app as flask_app # New import strategy

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    flask_app.config.update({
        "TESTING": True,
        # Add any other specific test configurations here
        # For example, if you were using a database:
        # "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    yield flask_app

# The 'client' fixture will be automatically provided by pytest-flask
# by using the 'app' fixture defined above.

# You can also define other fixtures here if needed, for example,
# to populate your mock database with specific test data before a test.
