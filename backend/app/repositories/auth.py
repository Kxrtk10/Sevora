from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserRole


class AuthRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_user_by_email(self, email: str) -> User | None:
        normalized_email = email.lower()
        statement = select(User).where(User.email == normalized_email)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        return await self.session.get(User, user_id)

    async def create_user(
        self,
        *,
        email: str,
        hashed_password: str,
        full_name: str,
        role: UserRole,
    ) -> User:
        user = User(
            email=email.lower(),
            hashed_password=hashed_password,
            full_name=full_name.strip(),
            role=role,
            status="active",
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
