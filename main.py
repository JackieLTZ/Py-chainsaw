from contextlib import asynccontextmanager
import logging
import sys
import time
import uvicorn
from fastapi import FastAPI, Request
from database import check_db_connection, create_tables, close
from api.routes import car_router, owner_router, admin_router
from starlette.middleware.base import BaseHTTPMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    try:
        await check_db_connection()
        print("Database connection successful")
        await create_tables()
        print("Tables created successfully")
    except Exception as e:
        print(f"Startup failed: {e}")
        sys.exit(1)

    try:
        yield
    finally:
        print("Shutting down...")
        try:
            await close()
            print("Database connection closed successfully")
        except Exception as e:
            print(f"Error during shutdown: {e}")

app = FastAPI(lifespan=lifespan)

app.include_router(router=car_router)
app.include_router(router=owner_router)
app.include_router(router=admin_router)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Middleware to log response time
class LogResponseTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()  
        response = await call_next(request)
        end_time = time.time()  

        response_time = (end_time - start_time) * 1000

        logger.info(f"Request: {request.method} {request.url.path}, "
                    f"Response Time: {response_time:.4f} ms")

        response.headers['X-Response-Time'] = str(response_time)

        return response

app.add_middleware(LogResponseTimeMiddleware)


@app.get("/")
def ping() -> dict[str, str]:
    return {"message": "pong"}


if __name__ == "__main__":
    uvicorn.run(app, port=8080)