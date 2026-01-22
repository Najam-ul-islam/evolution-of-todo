#!/usr/bin/env python3
"""
Test the authentication endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_endpoints():
    print("Testing authentication endpoints...")

    # Test register endpoint
    print("\n1. Testing registration endpoint:")
    try:
        register_resp = requests.post(f"{BASE_URL}/auth/register",
                                   json={"email": "test@example.com", "password": "password123"})
        print(f"   Register status: {register_resp.status_code}")
        print(f"   Register response: {register_resp.text}")
    except Exception as e:
        print(f"   Register error: {e}")

    # Test login endpoint
    print("\n2. Testing login endpoint:")
    try:
        login_resp = requests.post(f"{BASE_URL}/auth/login",
                                 json={"email": "test@example.com", "password": "password123"})
        print(f"   Login status: {login_resp.status_code}")
        print(f"   Login response: {login_resp.text}")
    except Exception as e:
        print(f"   Login error: {e}")

    # Test the root endpoint
    print("\n3. Testing root endpoint:")
    try:
        root_resp = requests.get(f"{BASE_URL}/../")
        print(f"   Root status: {root_resp.status_code}")
        print(f"   Root response: {root_resp.text}")
    except Exception as e:
        print(f"   Root error: {e}")

if __name__ == "__main__":
    test_endpoints()