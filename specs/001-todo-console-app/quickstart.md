# Quickstart Guide: Todo Console Application

## Setup
1. Ensure Python 3.13+ is installed
2. Install dependencies using UV: `uv sync` (or `uv pip install` for individual packages)
3. Run the application: `python src/main.py`

## Project Structure
```
src/
├── main.py              → CLI entry point
└── todo/
    ├── models.py        → Task model
    ├── service.py       → Task management logic
    └── cli.py           → CLI menu and input handling
```

## Basic Usage
1. Run `python src/main.py` to start the application
2. Use the menu options to perform operations:
   - Add Task: Enter title and optional description
   - View Tasks: See all tasks with IDs and status
   - Update Task: Modify existing task by ID
   - Delete Task: Remove task by ID
   - Mark Complete/Incomplete: Toggle task status by ID

## Development
- Business logic is in `service.py`
- Data models are in `models.py`
- User interface is in `cli.py`
- Main application flow is in `main.py`