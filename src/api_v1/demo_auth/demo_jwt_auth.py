from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from pydantic import BaseModel
from jose import JWTError

from src.api_v1.users.schemas import UserSchema
from src.auth import utils as auth_utils

# http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/demo_jwt_auth/jwt/login/")


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


router = APIRouter(prefix="/jwt", tags=["jwt"])

john = UserSchema(
    username="john",
    password=auth_utils.hash_password("qwerty"),
)

sam = UserSchema(
    username="sam",
    password=auth_utils.hash_password("12345"),
)


users_db: dict[str, UserSchema] = {
    john.username: john,
    sam.username: sam,
}


def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
):
    exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    if not (user := users_db.get(username)):
        raise exc

    if auth_utils.validate_password(password, user.password):
        return user

    raise exc


def get_current_token_payload(
    # cred: HTTPAuthorizationCredentials = Depends(http_bearer),
    token: str = Depends(oauth2_scheme),
) -> dict:
    # token = cred.credentials
    try:
        payload = auth_utils.decode_jwt(
            token,
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error",
        )
    return payload


def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


def get_current_active_auth_user(
    user: UserSchema = Depends(get_current_auth_user),
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Inactive user",
    )


@router.post("/login/", response_model=TokenInfo)
def auth_user_jwt(
    user: UserSchema = Depends(validate_auth_user),
):
    jwt_token = {
        # subject
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    token = auth_utils.encode_jwt(jwt_token)
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
        "email": user.email,
        "logged in at": iat,
    }
