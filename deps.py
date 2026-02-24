from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from config import secret_key, algorithm, accexx_token_exp_min
from database.userservice import get_user_by_username_db
from datetime import timedelta, datetime


oauth_schema = OAuth2PasswordBearer(tokenUrl="/token")


def _credentials_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"}
    )


async def get_current_user(request: Request, token: str | None = Depends(oauth_schema)):
    if not token:
        token = request.cookies.get("access_token")
        if token and token.startswith("Bearer "):
            token = token.split(" ", 1)[1]
    
    
    if not token:
        raise _credentials_exception()

    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username = payload.get("sub")
        if not username:
            raise _credentials_exception()
    except JWTError:
        raise _credentials_exception()
    user = get_user_by_username_db(username)
    if not user:
        raise _credentials_exception()
    return user



async def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=accexx_token_exp_min)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)

    return encoded_jwt









    


