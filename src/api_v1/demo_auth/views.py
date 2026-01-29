import secrets
import uuid
from typing import Any
from time import time

from fastapi import APIRouter, Depends, HTTPException, status, Header, Response, Cookie
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(tags=["Demo Auth"])
security = HTTPBasic()


@router.get("/basic_auth/")
def demo_auth(credentials: HTTPBasicCredentials = Depends(security)):
    return {
        "message": "Hi",
        "username": credentials.username,
        "password": credentials.password,
    }


users = {
    "admin": "admin",
    "user": "qwerty",
}

static_auth_token_to_username = {
    "10943a746560836dc30bce7ff19bd92f": "admin",
    "9d2b896eb539356f78b69e1ed4daa65a": "qwerty",
}


def get_auth(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
    )
    correct_pass = users.get(credentials.username)
    if correct_pass is None:
        raise exception

    if not secrets.compare_digest(
        correct_pass.encode("utf-8"),
        credentials.password.encode("utf-8"),
    ):
        raise exception

    return credentials.username


def get_username_by_static_auth_token(
    static: str = Header(alias="X-Static-Auth-Token"),
) -> str:
    if username := static_auth_token_to_username.get(static):
        return username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid",
    )


@router.get("/basic_auth_username/")
def demo_auth_username(username: str = Depends(get_auth)):
    return {
        "message": f"Hi, {username}",
    }


@router.get("/http_header_auth")
def demo_auth_http_header(
    username: str = Depends(get_username_by_static_auth_token),
):
    return {
        "message": f"Hi, {username}",
    }


COOKIES: dict[str, dict[str, Any]] = {}
COOKIE_SESSION_ID_KEY = "web_app_session_id"


def generate_session_id() -> str:
    return uuid.uuid4().hex


# dont use in real app


def get_session_data(
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
) -> dict:
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not authenticated",
        )
    return COOKIES[session_id]


@router.post("/login_cookie")
def demo_auth_login_cookies(
    response: Response,
    auth_username: str = Depends(get_auth),
    # auth_username: str = Depends(get_username_by_static_auth_token),
):
    session_id = generate_session_id()
    COOKIES[session_id] = {
        "username": auth_username,
        "time": int(time()),
    }
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
    return {"result": "ok 👍"}


@router.get("/check_cookie")
def demo_auth_check_cookies(
    user_session_data: dict = Depends(get_session_data),
):
    username = user_session_data["username"]
    return {
        "message": f"hello {username}",
        **user_session_data,
    }


@router.get("/delete_cookie")
def demo_auth_logout_cookies(
    response: Response,
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
    user_session_data: dict = Depends(get_session_data),
):
    COOKIES.pop(session_id, None)
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    username = user_session_data["username"]
    return {
        "message": f"bye {username}",
    }
