from fastapi import FastAPI
from routers import user, task

app = FastAPI()
app.include_router(user.router_user)
app.include_router(task.router_task)


@app.get("/")
def welcome():
    return {"message": "Welcome to Taskmanager"}
