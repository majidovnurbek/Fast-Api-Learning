from fastapi import FastAPI, APIRouter, HTTPException
from task_classroom.db import Database
from task_classroom.config import DATABASE_URL
from task_classroom.models import User
from pydantic import BaseModel

app = FastAPI()

# Database instance
db = Database(DATABASE_URL)
db.connect()
db.create_table()

router = APIRouter(prefix="/users")

class BaseResponse(BaseModel):
    data: dict

@app.on_event("shutdown")
def shutdown():
    db.close()

@router.get("/", response_model=list[User])
def get_users():
    """Barcha foydalanuvchilarni olish."""
    users = db.all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users


@router.post("/", response_model=User)
def create_user(user: User):
    """Yangi foydalanuvchi qo‘shish va qaytarish."""
    if db.is_exists(user.id):
        created_user = {
            "id": user.id,
            "full_name": user.full_name,
            "username": user.username,
            "email": user.email
        }
        raise HTTPException(status_code=400, detail=f"User already exists  {created_user}")

    db.add(user.id, user.full_name, user.username, user.email)

    # Qo‘shilgan userni qayta olish



@router.put("/{user_id}", response_model=BaseResponse)
def update_user(user_id: int, user: User):
    """Foydalanuvchini yangilash."""
    updated = db.update(user_id, user.full_name)
    if updated == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return BaseResponse(data={"message": f"User {user_id} updated successfully"})

@router.delete("/{user_id}", response_model=BaseResponse)
def delete_user(user_id: int):
    """Foydalanuvchini o‘chirish."""
    deleted = db.delete(user_id)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return BaseResponse(data={"message": f"User {user_id} deleted successfully"})

# Routerni ilovaga ulash
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
