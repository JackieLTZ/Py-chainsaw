
from typing import List
from pydantic import BaseModel, ConfigDict


class CarS(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    model: str
    price: int
    owner_id: int


class CarM(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    model: str
    price: int
    owner_id: int


class OwnerS(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    age: int


class OwnerM(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    age: int
    cars: List[CarM]  








