from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import Car
from api.schemas import CarS, CarM

async def get_cars(db: AsyncSession):
    result = await db.execute(select(Car).order_by(Car.id))
    cars =  result.scalars().all()

    cars_list = [CarM.model_validate(car) for car in cars]

    return cars_list

async def post_car(db: AsyncSession, car: CarS):
    new_car = Car(model=car.model, price=car.price, owner_id=car.owner_id)
    db.add(new_car)
    await db.commit()
    await db.refresh(new_car)
    return CarS.model_validate(new_car)

async def delete_cars(db: AsyncSession, car_id: int):

    result = await db.execute(select(Car).where(Car.id == car_id))
    car = result.scalar_one_or_none()

    if car is None:
        return None

    await db.delete(car)
    await db.commit()

    return 0

async def patch_car(db: AsyncSession, car_id: int, updated_body: CarS):

    result = await db.execute(select(Car).where(Car.id == car_id))

    car = result.scalar_one_or_none()

    if car is None:
        return None

    for key, value in updated_body.model_dump().items():
            setattr(car, key, value)
            
    await db.commit()

    await db.refresh(car)

    return car


