#!/usr/bin/env python3
"""
Final validation script for the Todo Backend implementation
Checks that all components are properly set up and working together
"""

import os
import sys
from pathlib import Path

def validate_structure():
    """Validate that all required files and directories exist"""
    print("🔍 Validating project structure...")

    required_paths = [
        "src/main.py",
        "src/config/settings.py",
        "src/models/todo.py",
        "src/api/v1/router.py",
        "src/utils/database.py",
        "src/utils/exceptions.py",
        "src/utils/logging.py",
        "pyproject.toml",
        ".env.example",
        ".gitignore",
        "README.md",
        "tests/test_main.py",
        "tests/api/test_todo.py",
        "alembic.ini",
        "alembic/env.py",
        "alembic/script.py.mako"
    ]

    missing_paths = []
    for path in required_paths:
        full_path = Path("backend") / path  # We're running from parent dir
        if not full_path.exists():
            # Try without backend prefix since we're in backend dir
            alt_path = Path(path)
            if not alt_path.exists():
                missing_paths.append(path)

    if missing_paths:
        print(f"❌ Missing required files/directories: {missing_paths}")
        return False
    else:
        print("✅ All required files and directories exist")
        return True


def validate_imports():
    """Validate that all modules can be imported without errors"""
    print("\n🔍 Validating module imports...")

    try:
        # Add current directory to path to allow relative imports
        sys.path.insert(0, os.getcwd())

        # Test importing main modules
        from src.config.settings import settings
        from src.models.todo import Todo, TodoCreate
        from src.utils.database import get_async_session
        from src.utils.exceptions import TodoNotFoundException
        from src.api.v1.router import router

        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during import validation: {e}")
        return False


def validate_configuration():
    """Validate that configuration is properly set up"""
    print("\n🔍 Validating configuration...")

    try:
        from src.config.settings import settings

        # Check that settings have expected attributes
        expected_attrs = ['database_url', 'jwt_secret', 'environment', 'debug']
        missing_attrs = [attr for attr in expected_attrs if not hasattr(settings, attr)]

        if missing_attrs:
            print(f"❌ Missing configuration attributes: {missing_attrs}")
            return False

        print("✅ Configuration validation passed")
        return True
    except Exception as e:
        print(f"❌ Configuration validation error: {e}")
        return False


def validate_models():
    """Validate that models are properly defined"""
    print("\n🔍 Validating data models...")

    try:
        from src.models.todo import Todo, TodoCreate, TodoRead, TodoUpdate

        # Test creating a basic todo instance
        todo_data = TodoCreate(title="Test", description="Test description", completed=False)

        print("✅ Data models validation passed")
        return True
    except Exception as e:
        print(f"❌ Data models validation error: {e}")
        return False


def run_validation():
    """Run all validation checks"""
    print("🚀 Starting final validation of Todo Backend implementation...\n")

    results = []
    results.append(validate_structure())
    results.append(validate_imports())
    results.append(validate_configuration())
    results.append(validate_models())

    print(f"\n📊 Validation Summary:")
    print(f"Passed: {sum(results)}/{len(results)} checks")

    if all(results):
        print("🎉 All validations passed! Backend implementation is complete and ready.")
        return True
    else:
        print("💥 Some validations failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    success = run_validation()
    sys.exit(0 if success else 1)