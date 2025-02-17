import uvicorn
from fastapi import FastAPI, HTTPException
from schemas import Car, CarM
app = FastAPI()



db: list[CarM] = []


@app.get("/")
def hello() -> dict[str, str]:
    return {"message": "hello"}

@app.get("/cars")
def show_car(price: int | None = None) -> list[CarM]:
    if price is not None:
        filtered_cars = [car for car in db if car.price >= price]
        return filtered_cars
    return db

@app.post("/{index}")
def create_car(car: Car, index: int) -> CarM:
    for car in db:
        if car.index == index:
            raise HTTPException(status_code=409, detail="Conflict: Car with this index already exists.")

    new_car = CarM(index=index, model=car.model, price=car.price)
    db.append(new_car)
    return new_car

@app.delete("/{index}")
def delete_car(index: int) -> dict[str, str]:
    for car in db:
        if car.index == index:
            db.remove(car)
            return {"message": f"Car by {car.index} index was successfully deleted"}

    raise HTTPException(status_code=404, detail="Car not found.")

@app.patch("/{index}")
def update_car(car: Car, index: int) -> CarM:
    for l_car in db:
        if l_car.index == index:

            # the updated_car was created for clarity XD
            updated_car = CarM(index=l_car.index, model=car.model, price=car.price)
            l_car.model = updated_car.model
            l_car.price = updated_car.price
            return updated_car

    raise HTTPException(status_code=404, detail="Car not found.")

if __name__ == "__main__":
    uvicorn.run(app, port=8080)