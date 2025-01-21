from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.models.users import User, UserAuth

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> User:
        return await self.get_user(email=email)
    
    async def get_user_by_username(self, username: str) -> User:
        return await self.get_user(username=username)

    async def get_user_by_id(self, user_id: int) -> User:
        return await self.get_user(id=user_id)

    async def get_user(self, **filters) -> User:
        query = select(User).filter_by(**filters)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create_user(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def create_user_auth(self, user_auth: UserAuth):
        self.db.add(user_auth)
        await self.db.commit()

    async def update_user(self, user: User) -> User:
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, user: User):
        await self.db.delete(user)
        await self.db.commit()
