# API Contracts: Todo Console Application

## Task Operations

### Add Task
- **Operation**: `add_task(title: str, description: str = None) -> Task`
- **Input**:
  - title (required, string)
  - description (optional, string)
- **Output**: Task object with assigned ID and pending status
- **Errors**: ValidationError if title is empty

### View All Tasks
- **Operation**: `get_all_tasks() -> List[Task]`
- **Input**: None
- **Output**: List of all Task objects
- **Errors**: None

### Update Task
- **Operation**: `update_task(task_id: int, title: str = None, description: str = None) -> Task`
- **Input**:
  - task_id (required, integer)
  - title (optional, string)
  - description (optional, string)
- **Output**: Updated Task object
- **Errors**: TaskNotFound if ID doesn't exist

### Delete Task
- **Operation**: `delete_task(task_id: int) -> bool`
- **Input**: task_id (required, integer)
- **Output**: Boolean indicating success
- **Errors**: TaskNotFound if ID doesn't exist

### Mark Task Complete
- **Operation**: `mark_task_complete(task_id: int) -> Task`
- **Input**: task_id (required, integer)
- **Output**: Updated Task object with completed status
- **Errors**: TaskNotFound if ID doesn't exist

### Mark Task Incomplete
- **Operation**: `mark_task_incomplete(task_id: int) -> Task`
- **Input**: task_id (required, integer)
- **Output**: Updated Task object with pending status
- **Errors**: TaskNotFound if ID doesn't exist

## Error Types
- **TaskNotFound**: Raised when operation references non-existent task ID
- **ValidationError**: Raised when input validation fails (e.g., empty title)