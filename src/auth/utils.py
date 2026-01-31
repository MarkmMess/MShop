from datetime import timedelta, datetime

import bcrypt

from jose import jwt

from src.core.config import settings


def encode_jwt(
    token: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.AuthJWT.algorithm,
    expire_minutes: int = settings.AuthJWT.expire_minutes,
    expire_timedelta: timedelta | None = None,
):
    to_encode = token.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encode = jwt.encode(
        token,
        private_key,
        algorithm,
    )
    return encode


def decode_jwt(
    token: dict,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.AuthJWT.algorithm,
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def validate_password(password: str, hashed_pass) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_pass)
