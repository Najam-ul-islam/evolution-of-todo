#!/usr/bin/env python3
"""
Test script for backend functionality testing.
Tests email signup/login, create/edit/delete todos, and signout functionality.
"""

import asyncio
import json
import sys
from typing import Dict, Optional
import httpx
import uuid


class TodoAPITester:
    """Class to test the Todo API functionality."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.user_id: Optional[str] = None

    async def register_user(self, email: str, password: str) -> Dict:
        """Register a new user."""
        print(f"Registering user: {email}")

        register_payload = {
            "email": email,
            "password": password
        }

        response = await self.client.post(
            f"{self.base_url}/api/auth/register",
            json=register_payload
        )

        print(f"Registration status: {response.status_code}")
        if response.status_code == 200:
            user_data = response.json()
            print(f"User registered successfully: {user_data['email']}")
            return user_data
        else:
            print(f"Registration failed: {response.text}")
            return {}

    async def login_user(self, email: str, password: str) -> Dict:
        """Login a user and store tokens."""
        print(f"Logging in user: {email}")

        login_payload = {
            "email": email,
            "password": password
        }

        response = await self.client.post(
            f"{self.base_url}/api/auth/login",
            json=login_payload
        )

        print(f"Login status: {response.status_code}")
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data["access_token"]
            self.refresh_token = token_data["refresh_token"]
            print("Login successful, tokens stored")

            # Get user ID from /me endpoint
            user_info = await self.get_current_user()
            if user_info:
                self.user_id = user_info.get('id')
                print(f"User ID obtained: {self.user_id}")

            return token_data
        else:
            print(f"Login failed: {response.text}")
            return {}

    async def get_current_user(self) -> Dict:
        """Get current user information."""
        if not self.access_token:
            print("No access token available")
            return {}

        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = await self.client.get(
            f"{self.base_url}/api/auth/me",
            headers=headers
        )

        print(f"Get current user status: {response.status_code}")
        if response.status_code == 200:
            user_data = response.json()
            print(f"Current user: {user_data['email']}")
            return user_data
        else:
            print(f"Failed to get current user: {response.text}")
            return {}

    async def create_todo(self, title: str, description: str = "", completed: bool = False) -> Dict:
        """Create a new todo."""
        if not self.access_token or not self.user_id:
            print("User not authenticated or user ID not available")
            return {}

        headers = {"Authorization": f"Bearer {self.access_token}"}
        todo_payload = {
            "title": title,
            "description": description,
            "completed": completed
        }

        response = await self.client.post(
            f"{self.base_url}/api/v2/users/{self.user_id}/tasks",
            json=todo_payload,
            headers=headers
        )

        print(f"Create todo status: {response.status_code}")
        if response.status_code == 201:
            todo_data = response.json()
            print(f"Todo created: {todo_data['title']}")
            return todo_data
        else:
            print(f"Failed to create todo: {response.text}")
            return {}

    async def get_todos(self) -> list:
        """Get all todos for the current user."""
        if not self.access_token or not self.user_id:
            print("User not authenticated or user ID not available")
            return []

        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = await self.client.get(
            f"{self.base_url}/api/v2/users/{self.user_id}/tasks",
            headers=headers
        )

        print(f"Get todos status: {response.status_code}")
        if response.status_code == 200:
            todos = response.json()
            print(f"Retrieved {len(todos)} todos")
            return todos
        else:
            print(f"Failed to get todos: {response.text}")
            return []

    async def get_todo(self, task_id: int) -> Dict:
        """Get a specific todo."""
        if not self.access_token or not self.user_id:
            print("User not authenticated or user ID not available")
            return {}

        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = await self.client.get(
            f"{self.base_url}/api/v2/users/{self.user_id}/tasks/{task_id}",
            headers=headers
        )

        print(f"Get todo status: {response.status_code}")
        if response.status_code == 200:
            todo = response.json()
            print(f"Retrieved todo: {todo['title']}")
            return todo
        else:
            print(f"Failed to get todo: {response.text}")
            return {}

    async def update_todo(self, task_id: int, title: str = None, description: str = None, completed: bool = None) -> Dict:
        """Update a specific todo."""
        if not self.access_token or not self.user_id:
            print("User not authenticated or user ID not available")
            return {}

        headers = {"Authorization": f"Bearer {self.access_token}"}

        # Prepare update payload with only provided fields
        update_payload = {}
        if title is not None:
            update_payload["title"] = title
        if description is not None:
            update_payload["description"] = description
        if completed is not None:
            update_payload["completed"] = completed

        response = await self.client.put(
            f"{self.base_url}/api/v2/users/{self.user_id}/tasks/{task_id}",
            json=update_payload,
            headers=headers
        )

        print(f"Update todo status: {response.status_code}")
        if response.status_code == 200:
            todo = response.json()
            print(f"Todo updated: {todo['title']}")
            return todo
        else:
            print(f"Failed to update todo: {response.text}")
            return {}

    async def delete_todo(self, task_id: int) -> bool:
        """Delete a specific todo."""
        if not self.access_token or not self.user_id:
            print("User not authenticated or user ID not available")
            return False

        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = await self.client.delete(
            f"{self.base_url}/api/v2/users/{self.user_id}/tasks/{task_id}",
            headers=headers
        )

        print(f"Delete todo status: {response.status_code}")
        if response.status_code == 204:
            print(f"Todo {task_id} deleted successfully")
            return True
        else:
            print(f"Failed to delete todo: {response.text}")
            return False

    async def logout(self) -> Dict:
        """Logout the current user."""
        print("Logging out user")
        response = await self.client.post(f"{self.base_url}/api/auth/logout")

        print(f"Logout status: {response.status_code}")
        if response.status_code == 200:
            logout_data = response.json()
            print("Logout successful")
            # Clear tokens
            self.access_token = None
            self.refresh_token = None
            self.user_id = None
            return logout_data
        else:
            print(f"Logout failed: {response.text}")
            return {}

    async def run_full_test(self):
        """Run the complete test sequence."""
        print("=" * 50)
        print("Starting Backend Functionality Test")
        print("=" * 50)

        # Generate a unique email for this test
        test_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
        test_password = "SecurePass123!"

        print(f"\nUsing test email: {test_email}")

        # Step 1: Register user
        print("\n--- Step 1: Register User ---")
        user_data = await self.register_user(test_email, test_password)
        if not user_data:
            print("Registration failed, aborting test")
            return False

        # Step 2: Login user
        print("\n--- Step 2: Login User ---")
        token_data = await self.login_user(test_email, test_password)
        if not token_data:
            print("Login failed, aborting test")
            return False

        # Step 3: Create a todo
        print("\n--- Step 3: Create Todo ---")
        todo1 = await self.create_todo("Test Todo 1", "This is the first test todo")
        if not todo1:
            print("Failed to create first todo")
            return False

        # Step 4: Create another todo
        print("\n--- Step 4: Create Another Todo ---")
        todo2 = await self.create_todo("Test Todo 2", "This is the second test todo", completed=True)
        if not todo2:
            print("Failed to create second todo")
            return False

        # Step 5: Get all todos
        print("\n--- Step 5: Get All Todos ---")
        todos = await self.get_todos()
        if len(todos) != 2:
            print(f"Expected 2 todos, got {len(todos)}")
            return False

        # Step 6: Get specific todo
        print("\n--- Step 6: Get Specific Todo ---")
        retrieved_todo = await self.get_todo(todo1['id'])
        if not retrieved_todo or retrieved_todo['title'] != "Test Todo 1":
            print("Failed to retrieve specific todo correctly")
            return False

        # Step 7: Update todo
        print("\n--- Step 7: Update Todo ---")
        updated_todo = await self.update_todo(todo1['id'], "Updated Test Todo 1", "Updated description", False)
        if not updated_todo or updated_todo['title'] != "Updated Test Todo 1":
            print("Failed to update todo correctly")
            return False

        # Step 8: Delete a todo
        print("\n--- Step 8: Delete Todo ---")
        delete_success = await self.delete_todo(todo2['id'])
        if not delete_success:
            print("Failed to delete todo")
            return False

        # Step 9: Verify deletion by getting all todos again
        print("\n--- Step 9: Verify Deletion ---")
        remaining_todos = await self.get_todos()
        if len(remaining_todos) != 1:
            print(f"After deletion, expected 1 todo, got {len(remaining_todos)}")
            return False

        # Step 10: Logout
        print("\n--- Step 10: Logout ---")
        logout_result = await self.logout()

        print("\n" + "=" * 50)
        print("Backend Functionality Test Completed Successfully!")
        print("=" * 50)

        return True

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


async def main():
    """Main function to run the test."""
    tester = TodoAPITester()

    try:
        success = await tester.run_full_test()
        if success:
            print("\n✅ All tests passed!")
        else:
            print("\n❌ Some tests failed!")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        await tester.close()


if __name__ == "__main__":
    asyncio.run(main())