from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.models.users import User, UserAuth, UserAuthProvider

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
    
    async def get_user_auth_by_user_id(self, user_id: int) -> UserAuth:
        query = select(UserAuth).filter_by(user_id=user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_user_by_oauth_provider(self, provider: str, provider_id: str) -> User:
        query = select(User).join(UserAuthProvider).where(
            UserAuthProvider.provider == provider,
            UserAuthProvider.provider_id == provider_id
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create_user_from_oauth(self, provider: str, provider_id: str, provider_token: str) -> User:
        async with self.db.begin():
            new_user = User(username=f"{provider}_{provider_id}", email=f"{provider}_{provider_id}@gmail.com")
            self.db.add(new_user)
            await self.db.flush([new_user])

            oauth_provider = UserAuthProvider(
                user_id=new_user.id,
                provider=provider,
                provider_id=provider_id,
                provider_token=provider_token,
            )
            self.db.add(oauth_provider)
            await self.db.flush([oauth_provider])

        return new_user

    async def create_user_from_oauth(self, new_user: User, oauth_provider: UserAuthProvider) -> User:
        try:
            self.db.add(new_user)
            await self.db.flush([new_user])

            oauth_provider.user_id = new_user.id
            self.db.add(oauth_provider)
            await self.db.flush([oauth_provider])

            await self.db.commit()
            return new_user
        except Exception as e:
            await self.db.rollback()
            return None
    
    async def create_user_and_auth(self, user: User, user_auth: UserAuth) -> User:
        try:
            self.db.add(user)
            await self.db.flush([user])

            user_auth.user_id = user.id
            self.db.add(user_auth)
            await self.db.flush([user_auth])

            await self.db.commit()
            return user
        except Exception as e:
            await self.db.rollback()
            return None
