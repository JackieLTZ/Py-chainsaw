from datetime import timedelta, timezone, datetime
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.schemas import TokenData
from database import get_db
from models import Admin

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "8456ea8c7ecbe085f4d9360a855c7b1ff17387e1621a8191d0d96bd4d53c990c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_admin(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Admin:
    from api.admin_crud import get_admin
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    admin = await get_admin(db, token_data.email)
    if admin is None:
        raise credentials_exception
    return admin

async def get_current_active_admin(
    current_admin: Admin = Depends(get_current_admin)
) -> Admin:
    return current_admin