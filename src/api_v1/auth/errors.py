from fastapi import HTTPException, status

not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Not found",
)
login_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
)
inactive = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Inactive user",
)
