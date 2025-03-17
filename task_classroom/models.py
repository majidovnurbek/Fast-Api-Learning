from pydantic import BaseModel

class User(BaseModel):
    id: int
    full_name: str
    username: str
    email: str
    password: str
