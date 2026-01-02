from pydantic import BaseModel, Field
from typing import Optional


class TaskCreate(BaseModel):
    """Schema for creating a task"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)


class TaskUpdate(BaseModel):
    """Schema for updating a task"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None


class Task(BaseModel):
    """Task response model"""
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Complete DevOps project",
                "description": "Build CI/CD pipeline with FastAPI",
                "completed": False
            }
        }
