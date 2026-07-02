import uuid 
from typing import Optional 
from fastapi import Depends , Request
from fastapi_users import BaseUserManager , FastAPIUsers , UUIDIDMixin , models
from fastapi_users.authentication import (
    AuthenticationBackend ,
    BearerTransport ,
    JWTStrategy
)

from fastapi_users.db import SQLAlchemyUserDatabase
from app.db import User, get_user_db

SSECRET = "7f6d8b9c3e2a1f4d5c6b8a9e0f1d2c3b4a5e6f7d8c9b0a1e2d3c4b5a6f7e8d9"

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_pass_token = SSECRET 
    verfication_token_secret = SSECRET
    async def on_after_register(
        self,
        user: User,
        request: Optional[Request] = None,
    ):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self,
        user: User,
        request: Optional[Request] = None,
    ):
        print(f"User {user.id} forgot their password.")

    async def on_after_request_verify(
        self,
        user: User,
        request: Optional[Request] = None,
    ):
        print(f"Verification requested for user {user.id}.")

async def get_user_manager(user_db : SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)

Bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
def get_jwt_Strategy():
    return JWTStrategy(secret=SSECRET , lifetime_seconds=36000)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=Bearer_transport ,
    get_strategy=get_jwt_Strategy
)

fastapi_users = FastAPIUsers[User , uuid.UUID](get_user_manager , auth_backends= [auth_backend] )
current_active_user = fastapi_users.current_user(active=True)