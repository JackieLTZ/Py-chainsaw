from pydantic import BaseModel, ConfigDict


class CarS(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    model: str
    price: int

class CarM(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    model: str
    price: int





