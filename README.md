# Todo Console Application

A clean, maintainable, in-memory todo application that runs in the terminal. No persistence to disk or database is allowed.

## Features

- Add tasks with titles and optional descriptions
- View all tasks with their completion status
- Update existing tasks
- Delete tasks
- Mark tasks as complete or incomplete
- Auto-incrementing task IDs
- In-memory storage (data is lost when application exits)

## Setup

1. Ensure you have Python 3.13+ installed
2. Install dependencies using UV:
   ```bash
   uv sync
   ```
   Or install directly with pip:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:

```bash
python src/main.py
```

The application will present a menu with the following options:
1. Add Task - Add a new task with a title and optional description
2. View All Tasks - Display all tasks with their ID and completion status
3. Update Task - Modify an existing task's title or description
4. Delete Task - Remove a task by its ID
5. Mark Task Complete - Mark a task as completed
6. Mark Task Incomplete - Mark a completed task as pending
7. Exit - Quit the application

## Project Structure

```
src/
├── main.py              # CLI entry point
└── todo/                # Todo application module
    ├── models.py        # Task model and data validation
    ├── service.py       # Task management business logic
    ├── cli.py           # CLI menu and input handling
    └── exceptions.py    # Custom exception classes
```

## Architecture

The application follows a clean architecture pattern:
- **Models layer**: Task entity definition and validation
- **Service layer**: Business logic for task operations
- **CLI layer**: User interface and input handling
- **Main entry point**: Application flow coordination

## Requirements

- Python 3.13+
- UV for dependency management (no external frameworks)
- No persistence to disk - all data stored in memory only
- Clean separation of UI and business logic
- Follows PEP-8 style guidelines