from enum import Enum
from pydantic import BaseModel


class ModelName(Enum):
    tesla = 'Tesla'
    bmw = 'BMW'
    li = 'Li'


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None