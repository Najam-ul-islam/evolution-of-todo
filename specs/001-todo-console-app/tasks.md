---
description: "Task list for Todo Console Application implementation"
---

# Tasks: Todo Console Application

**Input**: Design documents from `/specs/001-todo-console-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

<!--
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.

  The /sp.tasks command MUST replace these with actual tasks based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Endpoints from contracts/

  Tasks MUST be organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Delivered as an MVP increment

  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan in src/ directory
- [x] T002 Initialize Python project with UV dependencies in pyproject.toml
- [x] T003 [P] Configure linting and formatting tools (flake8, black, isort)

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [x] T004 Create Task model in src/todo/models.py with id, title, description, completed fields
- [x] T005 [P] Implement Task validation rules for title non-empty requirement
- [x] T006 Create in-memory TaskService in src/todo/service.py with next_id tracking
- [x] T007 Create custom exception classes in src/todo/exceptions.py for ValidationError and TaskNotFound
- [x] T008 Configure basic logging and error handling infrastructure

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---
## Phase 3: User Story 1 - Add and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new tasks and view all their tasks with proper ID and status indicators

**Independent Test**: Can be fully tested by adding several tasks and then viewing the complete list to verify they appear correctly with proper ID and status indicators

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T009 [P] [US1] Contract test for add_task operation in tests/unit/test_service.py
- [ ] T010 [P] [US1] Contract test for get_all_tasks operation in tests/unit/test_service.py

### Implementation for User Story 1

- [x] T011 [P] [US1] Implement add_task method in src/todo/service.py with auto-incrementing ID assignment
- [x] T012 [P] [US1] Implement get_all_tasks method in src/todo/service.py returning all tasks with status
- [x] T013 [US1] Create basic CLI menu structure in src/todo/cli.py for add/view operations
- [x] T014 [US1] Implement CLI input handling for adding tasks with title and optional description
- [x] T015 [US1] Implement CLI display of all tasks with ID, title, and completion status (✓/☐)
- [x] T016 [US1] Add validation and error handling for empty task titles

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---
## Phase 4: User Story 2 - Update and Delete Tasks (Priority: P2)

**Goal**: Enable users to modify or remove tasks after they've been created to correct mistakes or remove irrelevant tasks

**Independent Test**: Can be tested by creating tasks, updating their details, and verifying the changes persist; also by deleting tasks and confirming they no longer appear in the list

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T017 [P] [US2] Contract test for update_task operation in tests/unit/test_service.py
- [ ] T018 [P] [US2] Contract test for delete_task operation in tests/unit/test_service.py

### Implementation for User Story 2

- [x] T019 [P] [US2] Implement update_task method in src/todo/service.py allowing title/description updates
- [x] T020 [P] [US2] Implement delete_task method in src/todo/service.py removing tasks by ID
- [x] T021 [US2] Add CLI menu options for update and delete operations
- [x] T022 [US2] Implement CLI input handling for updating task details by ID
- [x] T023 [US2] Implement CLI input handling for deleting tasks by ID
- [x] T024 [US2] Add error handling for non-existent task IDs with appropriate user feedback

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---
## Phase 5: User Story 3 - Mark Tasks Complete/Incomplete (Priority: P3)

**Goal**: Enable users to track their progress by marking tasks as complete when finished, and potentially marking them as incomplete again

**Independent Test**: Can be tested by creating tasks, marking them complete, viewing them to confirm status change, and toggling back to incomplete

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T025 [P] [US3] Contract test for mark_task_complete operation in tests/unit/test_service.py
- [ ] T026 [P] [US3] Contract test for mark_task_incomplete operation in tests/unit/test_service.py

### Implementation for User Story 3

- [x] T027 [P] [US3] Implement mark_task_complete method in src/todo/service.py to set completion status
- [x] T028 [P] [US3] Implement mark_task_incomplete method in src/todo/service.py to clear completion status
- [x] T029 [US3] Add CLI menu options for mark complete/incomplete operations
- [x] T030 [US3] Implement CLI input handling for toggling task completion status by ID
- [x] T031 [US3] Add validation to prevent operations on non-existent tasks

**Checkpoint**: All user stories should now be independently functional

---
## Phase 6: Error Handling and Edge Cases

**Goal**: Implement proper handling of invalid inputs and edge cases as specified in the requirements

- [x] T032 Implement error handling for invalid menu choices with user-friendly messages
- [x] T033 Add comprehensive validation for all user inputs with appropriate error messages
- [x] T034 Implement graceful handling for non-existent task operations with clear feedback
- [ ] T035 [P] Add unit tests for all error handling scenarios in tests/unit/test_service.py
- [ ] T036 [P] Add integration tests for CLI error handling in tests/integration/test_cli.py

---
## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T037 [P] Documentation updates in README.md with setup and run instructions
- [x] T038 Code cleanup and refactoring to ensure PEP-8 compliance
- [ ] T039 [P] Additional unit tests in tests/unit/ for edge cases
- [ ] T040 Performance validation to ensure operations complete under 2 seconds
- [ ] T041 Run quickstart.md validation to ensure all features work as expected
- [x] T042 Create main application entry point in src/main.py to coordinate components

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Error Handling (Phase 6)**: Depends on all core user stories being implemented
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services (in foundational phase)
- Services before CLI interface
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---
## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---
## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence