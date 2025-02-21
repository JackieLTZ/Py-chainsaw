from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.owner_crud import get_owners, post_owners
from api.schemas import CarS, CarM, OwnerS
from api.car_crud import get_cars, post_car, delete_cars, patch_car
from database import get_db

car_router = APIRouter(tags=["Cars"])
owner_router = APIRouter(tags=["Owners"])

# CARS

@car_router.get("/cars")
async def read_cars(db: AsyncSession = Depends(get_db)):
    cars = await get_cars(db)
    return cars

@car_router.post("/cars", response_model=CarS)
async def create_car(car: CarS, db: AsyncSession = Depends(get_db)):
    return await post_car(db, car)

@car_router.delete("/cars{car_id}")
async def delete_car(car_id: int, db: AsyncSession = Depends(get_db)):
    car = await delete_cars(db, car_id)

    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    return {"message": "Car deleted successfully"}

@car_router.patch("/cars{car_id}", response_model=CarM)
async def update_car(car_id: int, body: CarS, db: AsyncSession = Depends(get_db)):
    car = await patch_car(car_id=car_id, updated_body=body, db=db)

    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    return car


# OWNERS

@owner_router.get("/owners")
async def read_owners(db: AsyncSession = Depends(get_db)):
    owners = await get_owners(db)

    return owners

@owner_router.post("/owners", response_model=OwnerS)
async def create_owner(owner: OwnerS, db: AsyncSession = Depends(get_db)):
    return await post_owners(db, owner)