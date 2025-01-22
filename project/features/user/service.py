from db.models.users import User, UserAuth
from features.user.repository import UserRepository
from features.user.schemas import UserCreate, UserResponse, UserUpdate
from utils.security import hash_password
from features.user.exceptions import UserNotFoundError, UserDeleteError, UserExistsError, UserCreateError, UserUpdateError

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    async def get_db_user(self, identifier) -> User:
        if isinstance(identifier, int):
            user = await self.user_repo.get_user_by_id(identifier)
        elif "@" in identifier:
            user = await self.user_repo.get_user_by_email(identifier)
        else:
            user = await self.user_repo.get_user_by_username(identifier)
        
        if not user:
            raise UserNotFoundError("Can not find user with identifier: {identifier}")

        return user

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        async def operations():
            # check if user already exists
            existing_user = await self.user_repo.get_user_by_email(user_data.email)
            if existing_user:
                raise UserExistsError("User already exists")

            username = user_data.username if user_data.username else user_data.email.split("@")[0]
            # create new user
            new_user = await self.user_repo.create_user(
                User(username=username, email=user_data.email)
            )

            # create new user auth
            await self.user_repo.create_user_auth(
                UserAuth(user_id=new_user.id, password=hash_password(user_data.password))
            )

            return new_user

        # execute operations inside a transaction
        new_user = await self.user_repo.execute_in_transaction(operations)

        if not new_user:
            raise UserCreateError("User create error")
        
        return UserResponse.model_validate(new_user)

    async def get_user(self, identifier) -> UserResponse:
        user = await self.get_db_user(identifier)

        if not user:
            raise UserNotFoundError("Can not find user with identifier: {identifier}")
        
        return UserResponse.model_validate(user)
    
    async def update_user(self, identifier, user_data: UserUpdate) -> UserResponse:
        user = await self.get_db_user(identifier)

        if not user:
            raise UserNotFoundError("Can not find user with identifier: {identifier}")
        
        # update user fields
        for field, value in user_data.model_dump(exclude_unset=True).items():
            if value is not None:  # only update fields that are not None
                setattr(user, field, value)

        # update user in database
        updated_user = await self.user_repo.update_user(user)

        if not updated_user:
            raise UserUpdateError("User update error")
        
        # validate and return updated user
        return UserResponse.model_validate(updated_user)

    async def delete_user(self, identifier):
        user = await self.get_db_user(identifier)     

        if not user:
            raise UserNotFoundError("Can not find user with identifier: {identifier}")
           
        await self.user_repo.delete_user(user)

        if user.status != "inactive":
            raise UserDeleteError("User delete error")

    async def get_all_users(self) -> list[UserResponse]:
        users = await self.user_repo.get_all_users()
        return [UserResponse.model_validate(user) for user in users]
