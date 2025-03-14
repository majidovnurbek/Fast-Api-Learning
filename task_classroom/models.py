from pydantic import BaseModel

class Users(BaseModel):
    fullname: str | None = None
    username: str | None = None
    email: str
    password: str