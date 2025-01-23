from db.models.users import User, UserAuth, UserAuthProvider
from features.user.repository import UserRepository
from features.auth.schemas import SignupRequest, LoginRequest, TokenResponse
from utils.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_refresh_token
from utils.oauth import OAuthProvider
from features.user.schemas import UserResponse
from features.user.exceptions import UserCreateError, UserNotFoundError, UserExistsError
from features.auth.exceptions import InvalidCredentialsError

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def sign_up(self, data: SignupRequest) -> UserResponse:
        # check if user already exists
        existing_user = await self.user_repo.get_user_by_email(data.email)
        if existing_user:
            raise UserExistsError("User already exists")

        username = data.email.split("@")[0]

        # create new user and auth
        new_user = await self.user_repo.create_user_and_auth(
            User(username=username, email=data.email), UserAuth(password=hash_password(data.password))
        )

        if not new_user:
            raise UserCreateError("Failed to create user")
        
        return UserResponse.model_validate(new_user)
    
    async def login_with_password(self, data: LoginRequest) -> TokenResponse:
        if data.email:
            user = await self.user_repo.get_user_by_email(data.email)
        else:
            user = await self.user_repo.get_user_by_username(data.username)

        if not user:
            raise UserNotFoundError("User not found")

        user_auth = await self.user_repo.get_user_auth_by_user_id(user.id)

        if not verify_password(data.password, user_auth.password):
            raise InvalidCredentialsError("Invalid credentials")

        access_token = create_access_token(data={"sub": user.email})
        refresh_token = create_refresh_token(data={"sub": user.email})

        return [TokenResponse(token=access_token, token_type="bearer"), TokenResponse(token=refresh_token, token_type=None)]
    
    async def refresh_token(self, refresh_token: str) -> TokenResponse:
        payload = decode_refresh_token(refresh_token)
        email = payload.get("sub")

        user = await self.user_repo.get_user_by_email(email)

        if not user:
            raise UserNotFoundError("User not found")

        access_token = create_access_token(data={"sub": user.email})
        return TokenResponse(token=access_token, token_type="bearer")
    
    async def login_with_oauth(self, provider: str, code: str) -> TokenResponse:
        # verify token
        if provider == "google":
            user_info = OAuthProvider.verify_google_token(code)
        elif provider == "line":
            user_info = OAuthProvider.verify_line_token(code)
        else:
            raise ValueError("Unsupported provider")

        # check if user already exists
        oauth_user = await self.user_repo.get_user_by_oauth_provider(
            provider=provider, provider_id=user_info["sub"]
        )

        if oauth_user:
            return TokenResponse(
                access_token=create_access_token({"id": oauth_user.id, "email": oauth_user.email}),
                token_type="bearer",
            )

        provider, provider_id, provider_token = provider, user_info["sub"], code
        
        # create new user
        new_user = await self.user_repo.create_user_from_oauth(
            User(username=f"{provider}_{provider_id}", email=f"{provider}_{provider_id}@gmail.com"),
            UserAuthProvider(provider=provider, provider_id=provider_id, provider_token=provider_token),
        )

        return TokenResponse(
            access_token=create_access_token({"id": new_user.id, "email": new_user.email}),
            token_type="bearer",
        )
    

    
    """
    async def sign_up(self, data: SignupRequest) -> UserResponse:
        async def operations():
            # check if user already exists
            existing_user = await self.user_repo.get_user_by_email(data.email)
            if existing_user:
                raise UserExistsError("User already exists")

            username = data.email.split("@")[0]

            # create new user
            new_user = await self.user_repo.create_user(
                User(username=username, email=data.email)
            )

            # create new user auth
            await self.user_repo.create_user_auth(
                UserAuth(user_id=new_user.id, password=hash_password(data.password))
            )

            return new_user

        # execute operations inside a transaction
        new_user = await self.user_repo.execute_in_transaction(operations)

        if not new_user:
            raise UserCreateError("Failed to create user")
        
        return UserResponse.model_validate(new_user)
    """
