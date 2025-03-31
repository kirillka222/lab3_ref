from fastapi import FastAPI

app = FastAPI()

todos = []

@app.post("/todos/")
def create_todo(task: str, priority: int = 1):
    todos.append({
        "id": len(todos) + 1,
        "task": task,
        "done": False,
        "priority": priority
    })
    return {"message": "Todo added"}

@app.get("/todos/")
def get_todos():
    return todos

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    if todo_id > len(todos) or todo_id < 1:
        return {"error": "Todo not found"}
    return todos[todo_id - 1]

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, task: str):
    if todo_id > len(todos) or todo_id < 1:
        return {"error": "Todo not found"}
    todos[todo_id - 1]["task"] = task
    return {"message": "Todo updated"}

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    if todo_id > len(todos) or todo_id < 1:
        return {"error": "Todo not found"}
    todos.pop(todo_id - 1)
    return {"message": "Todo deleted"}

@app.patch("/todos/{todo_id}/complete")
def complete_todo(todo_id: int):
    if todo_id > len(todos) or todo_id < 1:
        return {"error": "Todo not found"}
    todos[todo_id - 1]["done"] = True
    return {"message": "Todo completed"}

@app.get("/todos/priority/{level}")
def get_todos_by_priority(level: int):
    return [todo for todo in todos if todo["priority"] == level]

@app.get("/todos/count")
def count_todos():
    total = len(todos)
    done = sum(1 for todo in todos if todo["done"])
    return {
        "total": total,
        "done": done,
        "pending": total - done
    }