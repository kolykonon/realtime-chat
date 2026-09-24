from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from chat_service.core.config import get_settings
from chat_service.core.jwt import encode_jwt
from chat_service.schemas.token import Token
from chat_service.services.auth_service import AuthServiceDep

settings = get_settings()

router = APIRouter()


@router.post("/token")
async def get_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthServiceDep,
) -> Token:
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    payload = {"sub": str(user.id), "username": user.username}
    access_token = encode_jwt(
        payload,
        settings.security_settings.secret_key,
        token_type=settings.security_settings.access_token_type,
    )  # pyright: ignore[reportArgumentType]
    refresh_token = encode_jwt(
        payload,
        settings.security_settings.secret_key,
        token_type=settings.security_settings.refresh_token_type,
    )  # pyright: ignore[reportArgumentType]
    return Token(access_token=access_token, refresh_token=refresh_token)
