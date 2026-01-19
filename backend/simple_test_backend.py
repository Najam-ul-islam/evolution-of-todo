#!/usr/bin/env python3
"""
Simple test to verify backend functionality without database dependencies
"""

from fastapi.testclient import TestClient
from src.main import app

def test_basic_endpoints():
    """Test basic endpoints that don't require database"""
    client = TestClient(app)

    # Test root endpoint
    response = client.get("/")
    print(f"Root endpoint status: {response.status_code}")
    print(f"Root endpoint response: {response.json()}")
    assert response.status_code == 200

    # Test health endpoint
    response = client.get("/health")
    print(f"Health endpoint status: {response.status_code}")
    print(f"Health endpoint response: {response.json()}")
    assert response.status_code == 200

    print("Basic endpoints work correctly!")

if __name__ == "__main__":
    test_basic_endpoints()