from fastapi import FastAPI, HTTPException, status
from typing import List
from app.models import Task, TaskCreate, TaskUpdate

app = FastAPI(
    title="Task Manager API",
    description="A simple task management API with CI/CD pipeline",
    version="1.0.0"
)

# In-memory storage
tasks_db = {}
task_id_counter = 1


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Task Manager API",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "task-manager-api",
        "version": "1.0.0"
    }


@app.get("/tasks", response_model=List[Task], tags=["Tasks"])
async def get_all_tasks():
    """Get all tasks"""
    return list(tasks_db.values())


@app.get("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
async def get_task(task_id: int):
    """Get a specific task by ID"""
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return tasks_db[task_id]


@app.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    tags=["Tasks"]
)
async def create_task(task: TaskCreate):
    """Create a new task"""
    global task_id_counter

    new_task = Task(
        id=task_id_counter,
        title=task.title,
        description=task.description,
        completed=False
    )

    tasks_db[task_id_counter] = new_task
    task_id_counter += 1

    return new_task


@app.put("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
async def update_task(task_id: int, task_update: TaskUpdate):
    """Update an existing task"""
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    existing_task = tasks_db[task_id]

    # Update only provided fields
    if task_update.title is not None:
        existing_task.title = task_update.title
    if task_update.description is not None:
        existing_task.description = task_update.description
    if task_update.completed is not None:
        existing_task.completed = task_update.completed

    tasks_db[task_id] = existing_task
    return existing_task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Tasks"]
)
async def delete_task(task_id: int):
    """Delete a task"""
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    del tasks_db[task_id]
    return None


# Bonus: Statistics endpoint
@app.get("/tasks/stats/summary", tags=["Statistics"])
async def get_task_statistics():
    """Get task statistics"""
    total_tasks = len(tasks_db)
    completed_tasks = sum(1 for task in tasks_db.values() if task.completed)
    pending_tasks = total_tasks - completed_tasks

    return {
        "total": total_tasks,
        "completed": completed_tasks,
        "pending": pending_tasks,
        "completion_rate": (
            f"{(completed_tasks/total_tasks)*100:.1f}%"
            if total_tasks > 0 else "0%"
        )
    }
