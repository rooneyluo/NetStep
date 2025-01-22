from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.models.users import User, UserAuth

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def execute_in_transaction(self, operations: callable):
        """
        Executes a set of operations inside a single transaction.
        """
        async with self.db.begin():  # 自動管理 transaction
            try:
                result = await operations()
                await self.db.commit()  # 成功後提交交易
                return result
            except Exception as e:
                await self.db.rollback()  # 發生例外時回滾
                raise e

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
        await self.db.flush([user])
        return user

    async def create_user_auth(self, user_auth: UserAuth):
        self.db.add(user_auth)
        await self.db.flush([user_auth])
        return user_auth

    async def update_user(self, user: User) -> User:
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, user: User):
        user.status = "inactive"
        await self.db.commit()
        await self.db.refresh(user)

    async def get_all_users(self) -> list[User]:
        query = select(User)
        result = await self.db.execute(query)
        return result.scalars().all()
