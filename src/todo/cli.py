"""CLI interface for the Todo application."""

from typing import Optional
from .service import TaskService
from .models import Task


class TodoCLI:
    """Command-line interface for the Todo application."""

    def __init__(self):
        """Initialize the CLI with a task service."""
        self.service = TaskService()

    def run(self):
        """Run the main application loop."""
        print("Welcome to the Todo Console Application!")
        while True:
            self._display_menu()
            choice = input("Select an option (1-7): ").strip()

            if choice == '1':
                self._add_task()
            elif choice == '2':
                self._view_tasks()
            elif choice == '3':
                self._update_task()
            elif choice == '4':
                self._delete_task()
            elif choice == '5':
                self._mark_task_complete()
            elif choice == '6':
                self._mark_task_incomplete()
            elif choice == '7':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please select a number between 1-7.")

    def _display_menu(self):
        """Display the main menu options."""
        print("\n--- Todo Application ---")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete")
        print("6. Mark Task Incomplete")
        print("7. Exit")
        print("------------------------")

    def _add_task(self):
        """Add a new task."""
        print("\n--- Add Task ---")
        title = input("Enter task title: ").strip()

        if not title:
            print("Error: Task title cannot be empty.")
            return

        description_input = input("Enter task description (optional, press Enter to skip): ").strip()
        description = description_input if description_input else None

        try:
            task = self.service.add_task(title, description)
            print(f"✓ Task added successfully with ID {task.id}")
        except Exception as e:
            print(f"Error adding task: {e}")

    def _view_tasks(self):
        """Display all tasks."""
        print("\n--- All Tasks ---")
        tasks = self.service.get_all_tasks()

        if not tasks:
            print("No tasks found.")
            return

        for task in tasks:
            status = "✓" if task.completed else "☐"
            print(f"ID: {task.id} | {status} | Title: {task.title}")
            if task.description:
                print(f"      Description: {task.description}")
        print("-----------------")

    def _update_task(self):
        """Update an existing task."""
        print("\n--- Update Task ---")
        try:
            task_id = int(input("Enter task ID to update: ").strip())
        except ValueError:
            print("Error: Please enter a valid task ID (number).")
            return

        # Check if task exists first
        try:
            current_task = self.service.get_task_by_id(task_id)
        except Exception:
            print(f"Error: Task with ID {task_id} does not exist.")
            return

        print(f"Current task: {current_task.title}")
        if current_task.description:
            print(f"Current description: {current_task.description}")

        new_title = input(f"Enter new title (or press Enter to keep '{current_task.title}'): ").strip()
        new_title = new_title if new_title else None

        new_description = input(f"Enter new description (or press Enter to keep current): ").strip()
        new_description = new_description if new_description else None

        try:
            updated_task = self.service.update_task(task_id, new_title, new_description)
            print(f"✓ Task {updated_task.id} updated successfully")
        except Exception as e:
            print(f"Error updating task: {e}")

    def _delete_task(self):
        """Delete a task."""
        print("\n--- Delete Task ---")
        try:
            task_id = int(input("Enter task ID to delete: ").strip())
        except ValueError:
            print("Error: Please enter a valid task ID (number).")
            return

        try:
            self.service.delete_task(task_id)
            print(f"✓ Task with ID {task_id} deleted successfully")
        except Exception as e:
            print(f"Error deleting task: {e}")

    def _mark_task_complete(self):
        """Mark a task as complete."""
        print("\n--- Mark Task Complete ---")
        try:
            task_id = int(input("Enter task ID to mark complete: ").strip())
        except ValueError:
            print("Error: Please enter a valid task ID (number).")
            return

        try:
            task = self.service.mark_task_complete(task_id)
            print(f"✓ Task '{task.title}' marked as complete")
        except Exception as e:
            print(f"Error marking task complete: {e}")

    def _mark_task_incomplete(self):
        """Mark a task as incomplete."""
        print("\n--- Mark Task Incomplete ---")
        try:
            task_id = int(input("Enter task ID to mark incomplete: ").strip())
        except ValueError:
            print("Error: Please enter a valid task ID (number).")
            return

        try:
            task = self.service.mark_task_incomplete(task_id)
            print(f"✓ Task '{task.title}' marked as incomplete")
        except Exception as e:
            print(f"Error marking task incomplete: {e}")