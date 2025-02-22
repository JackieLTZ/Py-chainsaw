from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.admin_crud import authenticate_admin, get_admin
from api.owner_crud import get_owners, post_owners, delete_owners
from api.schemas import CarS, CarM, OwnerS, Token
from api.car_crud import get_cars, post_car, delete_cars, patch_car
from database import get_db
from models import Admin
from utils.jwt_setup import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_active_admin, verify_password

car_router = APIRouter(tags=["Cars"])
owner_router = APIRouter(tags=["Owners"])
admin_router = APIRouter(tags=["Admin"])

# CARS

@car_router.get("/cars")
async def read_cars(db: AsyncSession = Depends(get_db)):
    cars = await get_cars(db)
    return cars

@car_router.post("/cars", response_model=CarS)
async def create_car(car: CarS, db: AsyncSession = Depends(get_db)):
    return await post_car(db, car)

@car_router.delete("/cars/{car_id}")
async def delete_car(car_id: int, db: AsyncSession = Depends(get_db)):
    car = await delete_cars(db, car_id)

    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    return {"message": "Car deleted successfully"}

@car_router.patch("/cars/{car_id}", response_model=CarM)
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

@owner_router.delete("/owners{owner_id}")
async def remove_owner(owner_id: int, db: AsyncSession = Depends(get_db)):
    car = await delete_owners(db, owner_id)

    if car is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    
    return {"message": "Owner removed successfully"}

@admin_router.post("/token")
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
):
    # Use form_data.username as an email
    admin = await get_admin(db, form_data.username)

    if not admin or not verify_password(form_data.password, admin.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@admin_router.get("/admin/me")
async def read_me(current_admin: Annotated[Admin, Depends(get_current_active_admin)]):
    return current_admin