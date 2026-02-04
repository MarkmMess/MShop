from pydantic import BaseModel, ConfigDict, EmailStr


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    hashed_password: str
    email: EmailStr
    active: bool = True
