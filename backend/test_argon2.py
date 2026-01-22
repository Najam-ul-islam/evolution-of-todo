#!/usr/bin/env python3
"""
Test script to check if argon2 is working properly
"""
from src.utils.security import hash_password, verify_password

def test_argon2():
    print("Testing argon2 password hashing...")

    try:
        # Test hashing
        password = "Password123"
        print(f"Original password: {password}")

        hashed = hash_password(password)
        print(f"Hashed password: {hashed}")

        # Test verification
        is_valid = verify_password(password, hashed)
        print(f"Verification result: {is_valid}")

        if hashed and is_valid:
            print("✅ Argon2 is working correctly!")
        else:
            print("❌ Argon2 is not working properly")

    except Exception as e:
        print(f"❌ Error with argon2: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_argon2()