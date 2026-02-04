from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from models import db_helper
from . import crud
from .errors import not_found, login_exc, inactive
from src.api_v1.auth.schemas import UserSchema
import src.api_v1.auth.security as auth_security

# http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/demo_jwt_auth/jwt/login/")


router = APIRouter(prefix="/jwt", tags=["jwt"])


async def validate_auth_user(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    username: str = Form(...),
    password: str = Form(...),
) -> UserSchema:
    user = await crud.get_user(session, username)
    if not user:
        raise not_found
    if not auth_security.validate_password(password, user.hashed_password):
        raise login_exc
    return user


def get_current_token_payload(
    # cred: HTTPAuthorizationCredentials = Depends(http_bearer),
    token: str = Depends(oauth2_scheme),
) -> dict:
    # token = cred.credentials
    try:
        payload = auth_security.decode_jwt(
            token,
        )
    except JWTError:
        raise login_exc
    return payload


async def get_current_auth_user(
    session: AsyncSession,
    payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    username: str | None = payload.get("sub")
    if user := await crud.get_user(session, username):
        return user
    raise not_found


def get_current_active_auth_user(
    user: UserSchema = Depends(get_current_auth_user),
):
    if user.active:
        return user
    raise inactive
