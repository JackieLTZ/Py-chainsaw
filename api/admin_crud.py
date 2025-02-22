
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Admin
from utils.jwt_setup import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_admin(db: AsyncSession, email: str):
    result = await db.execute(select(Admin).where(Admin.email == email))

    admin = result.scalar_one_or_none()


    return admin

async def authenticate_admin(db: AsyncSession, email: str, password: str):
    admin = await get_admin(db, email)

    if admin is None:
        return None
    if not verify_password(password, admin.password):
        return None

    return admin

