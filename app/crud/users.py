from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    func,
    select,
    case
)

from app.models import (
    User,
    UserRole
)
from app.schemas import (
    UserListAdmin,
    UserListView
)


# Admin

async def get_users_admin(
        page: int,
        session: AsyncSession
) -> UserListAdmin:
    total_stmt = select(func.count(case((User.role == UserRole.customer, 1))))
    total_result = await session.execute(total_stmt)
    total = total_result.scalar_one()
    stmt = (
        select(User)
        .where(User.role == UserRole.customer)
        .order_by(-User.id)
        .offset((page - 1) * 25)
        .limit(25)
    )
    result = await session.execute(stmt)
    users = result.scalars().all()
    return UserListAdmin(
        data=[UserListView.model_validate(user) for user in users],
        total=total,
        initial=(page - 1) * 25 + 1 if users else 0,
        last=(page - 1) * 25 + len(users),
        total_pages=(total + 25 - 1) // 25,
        page=page
    )
