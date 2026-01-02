import pytest
from fastapi.testclient import TestClient
from app.main import app
import app.main

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    """Reset database before each test"""
    app.main.tasks_db.clear()
    app.main.task_id_counter = 1
    yield
    app.main.tasks_db.clear()


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "task-manager-api"


def test_get_all_tasks_empty():
    """Test getting tasks when database is empty"""
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_create_task():
    """Test creating a new task"""
    task_data = {
        "title": "Test Task",
        "description": "This is a test task"
    }
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["completed"] is False
    assert "id" in data


def test_create_task_without_description():
    """Test creating task with only title"""
    task_data = {"title": "Simple Task"}
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Simple Task"
    assert data["description"] is None


def test_create_task_invalid_data():
    """Test creating task with empty title fails"""
    task_data = {"title": ""}
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 422  # Validation error


def test_get_specific_task():
    """Test getting a specific task"""
    # Create a task first
    create_response = client.post("/tasks", json={
        "title": "Get This Task"
    })
    task_id = create_response.json()["id"]

    # Get the task
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Get This Task"


def test_get_nonexistent_task():
    """Test getting a task that doesn't exist"""
    response = client.get("/tasks/9999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_task():
    """Test updating a task"""
    # Create a task
    create_response = client.post("/tasks", json={
        "title": "Original Title"
    })
    task_id = create_response.json()["id"]

    # Update the task
    update_data = {
        "title": "Updated Title",
        "completed": True
    }
    response = client.put(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["completed"] is True


def test_update_nonexistent_task():
    """Test updating a task that doesn't exist"""
    response = client.put("/tasks/9999", json={"title": "New Title"})
    assert response.status_code == 404


def test_delete_task():
    """Test deleting a task"""
    # Create a task
    create_response = client.post("/tasks", json={
        "title": "Task to Delete"
    })
    task_id = create_response.json()["id"]

    # Delete it
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    # Verify it's gone
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_task():
    """Test deleting a task that doesn't exist"""
    response = client.delete("/tasks/9999")
    assert response.status_code == 404


def test_task_statistics():
    """Test task statistics endpoint"""
    # Create some tasks
    client.post("/tasks", json={"title": "Task 1"})
    client.post("/tasks", json={"title": "Task 2"})
    client.put("/tasks/1", json={"completed": True})

    # Get statistics
    response = client.get("/tasks/stats/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert data["completed"] == 1
    assert data["pending"] == 1
    assert "50.0%" in data["completion_rate"]


def test_multiple_tasks_creation():
    """Test creating multiple tasks"""
    tasks = [
        {"title": "Task 1", "description": "First task"},
        {"title": "Task 2", "description": "Second task"},
        {"title": "Task 3", "description": "Third task"}
    ]

    for task in tasks:
        response = client.post("/tasks", json=task)
        assert response.status_code == 201

    # Get all tasks
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 3