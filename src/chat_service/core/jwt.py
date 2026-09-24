import datetime
from typing import Any, Literal

import jwt

from chat_service.core.config import get_settings

settings = get_settings()

def encode_jwt(
    payload: dict[str,Any],
    secret: str,
    algorithm: str = settings.security_settings.algorithm,
    token_type: Literal['access', 'refresh'] = settings.security_settings.access_token_type  # pyright: ignore[reportArgumentType] опять пайрайт ругается
) -> str:
    new_payload = payload.copy()
    new_payload.update(
        iat=datetime.datetime.now(datetime.UTC),
        type=token_type,
    )
    if token_type == settings.security_settings.access_token_type:
        new_payload.update(
            exp=datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=int(settings.security_settings.access_token_expire_minutes))  # pyright: ignore[reportArgumentType]
        )
    elif token_type == settings.security_settings.refresh_token_type:
        new_payload.update(
            exp=datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=int(settings.security_settings.refresh_token_expire_days))  # pyright: ignore[reportArgumentType]
        )
    else:
        raise ValueError(f"Unknown token type: {token_type}")

    return jwt.encode(
        payload=new_payload,
        key=secret,
        algorithm=algorithm,
    )

def decode_jwt(
    token: str,
    secret: str,
    algorithm: str = settings.security_settings.algorithm,
) -> dict[str, Any]:
    return jwt.decode(
        token,
        key=secret,
        algorithms=[algorithm],
    )
