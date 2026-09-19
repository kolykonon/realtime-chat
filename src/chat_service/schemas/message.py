from pydantic import BaseModel

class MessageRead(BaseModel):
    text: str

class MessageCreate(BaseModel):
    text: str

