from fastapi import FastAPI, HTTPException
from typing import List, Dict

app = FastAPI()

TodoItem = Dict[str, object]
TodoList = List[TodoItem]

todos_db: TodoList = []


def find_todo_by_id(todo_id: int) -> TodoItem:
    if todo_id < 1 or todo_id > len(todos_db):
        raise HTTPException(
            status_code=404,
            detail=f"Задача с ID {todo_id} не найдена"
        )
    return todos_db[todo_id - 1]


def check_priority_value(priority: int):
    if priority not in {1, 2, 3}:
        raise HTTPException(
            status_code=400,
            detail="Приоритет должен быть числом от 1 до 3"
        )


@app.post("/todos/", status_code=201)
def add_new_todo(task: str, priority: int = 1) -> Dict[str, str]:
    check_priority_value(priority)

    new_task = {
        "id": len(todos_db) + 1,
        "task": task,
        "done": False,
        "priority": priority
    }
    todos_db.append(new_task)
    return {"message": "Новая задача добавлена"}


@app.get("/todos/", response_model=TodoList)
def get_all_todos() -> TodoList:
    return todos_db


@app.get("/todos/{todo_id}", response_model=TodoItem)
def get_single_todo(todo_id: int) -> TodoItem:
    return find_todo_by_id(todo_id)


@app.put("/todos/{todo_id}")
def update_todo_text(todo_id: int, task: str) -> Dict[str, str]:
    todo = find_todo_by_id(todo_id)
    todo["task"] = task
    return {"message": "Текст задачи обновлён"}


@app.delete("/todos/{todo_id}")
def remove_todo(todo_id: int) -> Dict[str, str]:
    find_todo_by_id(todo_id)
    todos_db.pop(todo_id - 1)
    return {"message": "Задача удалена"}


@app.patch("/todos/{todo_id}/complete")
def mark_todo_completed(todo_id: int) -> Dict[str, str]:
    todo = find_todo_by_id(todo_id)
    todo["done"] = True
    return {"message": "Задача помечена как выполненная"}


@app.get("/todos/priority/{level}", response_model=TodoList)
def filter_todos_by_priority(level: int) -> TodoList:
    check_priority_value(level)
    return [todo for todo in todos_db if todo["priority"] == level]


@app.get("/todos/count")
def count_todos_stats() -> Dict[str, int]:
    completed = sum(1 for todo in todos_db if todo["done"])
    total = len(todos_db)

    return {
        "total": total,
        "completed": completed,
        "pending": total - completed
    }