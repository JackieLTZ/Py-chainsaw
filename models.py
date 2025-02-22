from typing import List

from pydantic import validators
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship




class Base(DeclarativeBase):
    pass


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True)
    model: Mapped[str]
    price: Mapped[int]
    owner_id: Mapped[int] = mapped_column(ForeignKey("owners.id"))
    owner: Mapped["Owner"] = relationship("Owner", back_populates="cars")


class Owner(Base):
    __tablename__ = "owners"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    age: Mapped[int] = mapped_column()
    cars: Mapped[List["Car"]] = relationship("Car", back_populates="owner")

class Admin(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()


    