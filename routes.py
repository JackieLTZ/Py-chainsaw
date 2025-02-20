from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import CarS, CarM
from crud import get_cars, post_car, delete_cars, patch_car
from database import get_db

router = APIRouter()

@router.get("/cars")
async def read_cars(db: AsyncSession = Depends(get_db)):
    cars = await get_cars(db)
    return cars

@router.post("/cars", response_model=CarS)
async def create_car(car: CarS, db: AsyncSession = Depends(get_db)):
    return await post_car(db, car)

@router.delete("/cars{car_id}")
async def delete_car(car_id: int, db: AsyncSession = Depends(get_db)):
    car = await delete_cars(db, car_id)

    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    return {"message": "Car deleted successfully"}

@router.patch("/cars{car_id}", response_model=CarM)
async def update_car(car_id: int, body: CarS, db: AsyncSession = Depends(get_db)):
    car = await patch_car(car_id=car_id, updated_body=body, db=db)

    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    return car
