"""
Pytest configuration and shared fixtures for all tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Provide a TestClient instance for making requests to the app."""
    return TestClient(app)
