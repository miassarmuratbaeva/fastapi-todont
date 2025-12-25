from fastapi.routing import APIRouter
from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/tasks", tags=["tasks"])
app = FastAPI()
tags = ["tasks"]

class Task(BaseModel):
    id: int
    title: str
    descriptional: Optional[str] = None
    done: bool = False

tasks = []

@router.post("/" , response_model=Task)
def create_task(task: Task):
    tasks.append(task)
    return task


@router.get("/" , response_model=List[Task])
def get_task_list():
    return tasks

@router.get("/{pk}", response_model=Task)
def get_one_task(pk: int):
    for task in tasks:
        if task.id == pk:
            return task
    raise
HTTPException(status_code=404, detail="Task not found")


@router.put("/{pk}" , response_model=Task)
def update_task(pk: int, updated_task: Task):
    for index, task in enumerate(tasks):
        if task.id == pk:
            tasks[index] = updated_task
            return updated_task
    raise 
HTTPException(status_code=404, detail="Task not found")

@router.delete("/{pk}")
def delete_task(pk: int):
    for index, task in enumerate(tasks):
        if task.id == pk:
            del tasks[index]
            return {"detail": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")

app.include_router(router)