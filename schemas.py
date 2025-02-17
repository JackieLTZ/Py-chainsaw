from pydantic import BaseModel


class Car(BaseModel):
    model: str
    price: int

class CarM(BaseModel):
    index: int
    model: str
    price: int



