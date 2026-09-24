from typing import Annotated

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from chat_service.core.config import SettingsDep
from chat_service.core.jwt import decode_jwt
from chat_service.db.models import User
from chat_service.services.user_service import UserServiceDep

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")


async def get_current_user(
    settings: SettingsDep,
    user_service: UserServiceDep,
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = decode_jwt(
            token,
            settings.security_settings.secret_key,
            settings.security_settings.algorithm,
        )  # pyright: ignore[reportArgumentType]
        id = payload.get("sub")
        if not id:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = await user_service.get(int(id))
    if not user:
        raise credentials_exception
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
