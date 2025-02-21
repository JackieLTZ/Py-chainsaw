from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import OwnerM, OwnerS
from models import Owner


async def get_owners(db: AsyncSession):
    result = await db.execute(
        select(Owner)
        .options(selectinload(Owner.cars))
        .order_by(Owner.id)
    )
    owners = result.scalars().all()

    owners_list = [OwnerM.model_validate(owner) for owner in owners]

    return owners_list


async def post_owners(db: AsyncSession, owner: OwnerS):
    new_owner = Owner(name=owner.name, age=owner.age)
    db.add(new_owner)
    await db.commit()
    await db.refresh(new_owner)

    return OwnerS.model_validate(new_owner)