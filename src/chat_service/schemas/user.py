from pydantic import BaseModel


class UserRead(BaseModel):
    username: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    password: str


class UserCreateDB(BaseModel):
    username: str
    hashed_password: str


class UserUpdate(BaseModel):
    username: str | None
    password: str | None

    class Config:
        from_attributes = True
