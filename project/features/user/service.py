from db.models.users import User, UserAuth
from features.user.repository import UserRepository
from features.user.schemas import UserCreate, UserResponse
from core.security import hash_password

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        # check if user already exists
        existing_user = await self.user_repo.get_user_by_email(user_data.email)
        if existing_user:
            raise ValueError("User already exists")

        # create new user
        new_user = User(
            username=user_data.email,
            email=user_data.email,
        )

        created_user = await self.user_repo.create_user(new_user, hash_password(user_data.password))

        new_auth = UserAuth(
            user_id=created_user.id,
            password=hash_password(user_data.password)
        )

        self.user_repo.create_user_auth(new_auth)
        
        return UserResponse.model_validate(created_user)

    async def get_user(self, identifier: str | int) -> UserResponse:
        if isinstance(identifier, int):
            user = await self.user_repo.get_user_by_id(identifier)
        elif "@" in identifier:
            user = await self.user_repo.get_user_by_email(identifier)
        else:
            user = await self.user_repo.get_user_by_username(identifier)
        
        if not user:
            raise ValueError("User not found")

        return UserResponse.model_validate(user)