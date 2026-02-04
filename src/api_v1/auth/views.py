from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from sqlalchemy.ext.asyncio import AsyncSession

from models import db_helper
from .schemas import TokenInfo, CreateUser
from service import (
    validate_auth_user,
    get_current_token_payload,
    get_current_active_auth_user,
)
from . import crud
from src.api_v1.auth.schemas import UserSchema
import src.api_v1.auth.security as auth_security

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/jwt/login/new")


router = APIRouter(prefix="/jwt", tags=["jwt"])


@router.post("/signIn", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: CreateUser,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_user(session, user)


# @router.get("/get/user")
# async def get_user_by_name(
#     session: AsyncSession = Depends(db_helper.scoped_session_dependency),
# ):
#     return await get_user(session, "admin")


@router.post("/login/new/", response_model=TokenInfo)
async def auth_user_jwt(
    user: UserSchema = Depends(validate_auth_user),
):
    jwt_token = {
        # subject
        "sub": user.username,
        "username": user.username,
    }
    token = auth_security.encode_jwt(jwt_token)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )


@router.get("/user/i/")
def auth_user_check_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserSchema = Depends(get_current_active_auth_user),
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "logged in at": iat,
    }
