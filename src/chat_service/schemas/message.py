from pydantic import BaseModel


class MessageRead(BaseModel):
    text: str

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    text: str

    class Config:
        from_attributes = True
