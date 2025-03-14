import os
from fastapi import FastAPI
from task_classroom.models import Users
from .db import Database
from dotenv import load_dotenv

load_dotenv()

db = Database(
    db_file=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)
app=FastAPI()

@app.get("/api/users/")
async def get_users():
    ...


@app.post("/api/users/")
async def create_user(user: Users):
    if db.check_user(user.username):
        return {"error": "Username already exists"}
    try:
        db.add_user(user.fullname, user.username, user.email, user.password)
        return {"success": True, "data": user}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.put("/api/users/{user_id}")
async def update_user():
    ...

@app.delete("/api/users/{user_id}")
async def delete_user():
    ...
