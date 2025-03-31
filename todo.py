from fastapi import FastAPI, HTTPException
from typing import List, Dict

app = FastAPI()

Todo = Dict[str, object]
TodoList = List[Todo]

todos_db: TodoList = []


def _get_todo(todo_id: int) -> Todo:
    try:
        return todos_db[todo_id - 1]
    except IndexError:
        raise HTTPException(status_code=404, detail="Todo not found")


def _validate_priority(priority: int):
    if not 1 <= priority <= 3:
        raise HTTPException(
            status_code=400,
            detail="Priority must be between 1 and 3"
        )


# Эндпоинты
@app.post("/todos/", status_code=201)
def create_todo(task: str, priority: int = 1) -> Dict[str, str]:
    _validate_priority(priority)

    new_todo = {
        "id": len(todos_db) + 1,
        "task": task,
        "done": False,
        "priority": priority
    }
    todos_db.append(new_todo)
    return {"message": "Todo added"}


@app.get("/todos/", response_model=TodoList)
def get_todos() -> TodoList:
    return todos_db


@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int) -> Todo:
    return _get_todo(todo_id)


@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, task: str) -> Dict[str, str]:
    todo = _get_todo(todo_id)
    todo["task"] = task
    return {"message": "Todo updated"}


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int) -> Dict[str, str]:
    _get_todo(todo_id)
    todos_db.pop(todo_id - 1)
    return {"message": "Todo deleted"}


@app.patch("/todos/{todo_id}/complete")
def complete_todo(todo_id: int) -> Dict[str, str]:
    todo = _get_todo(todo_id)
    todo["done"] = True
    return {"message": "Todo completed"}


@app.get("/todos/priority/{level}", response_model=TodoList)
def get_todos_by_priority(level: int) -> TodoList:
    _validate_priority(level)
    return [todo for todo in todos_db if todo["priority"] == level]


@app.get("/todos/count")
def count_todos() -> Dict[str, int]:
    done_count = sum(1 for todo in todos_db if todo["done"])
    return {
        "total": len(todos_db),
        "done": done_count,
        "pending": len(todos_db) - done_count
    }