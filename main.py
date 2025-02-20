from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from database import create_tables, close
from schemas import CarM
from routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔄 Creating database tables...")
    await create_tables()
    yield
    print("🛑 Closing database connection...")
    await close()
    pass

app = FastAPI(lifespan=lifespan)

app.include_router(router=router)


db: list[CarM] = []


@app.get("/")
def hello() -> dict[str, str]:
    return {"message": "hello"}



if __name__ == "__main__":
    uvicorn.run(app, port=8080)