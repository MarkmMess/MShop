from fastapi import APIRouter, Depends, Form, HTTPException
from pydantic import BaseModel
from starlette import status

from src.api_v1.users.schemas import UserSchema
from src.auth import utils as auth_utils


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
