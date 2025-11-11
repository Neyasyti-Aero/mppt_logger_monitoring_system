from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class UserBase(BaseModel):
    username: str
    tg_id: Optional[int] = None

class UserCreate(UserBase):
    password: str
    role: str = "user"

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    role: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class LoggerBase(BaseModel):
    identifier: str
    description: Optional[str] = None

class LoggerCreate(LoggerBase):
    pass

class Logger(LoggerBase):
    id: int
    class Config:
        from_attributes = True

class LoggerDataCreate(BaseModel):
    identifier: str
    voltage: float
    current: float
    power: float
    illuminance: float
    isMaxPoint: Optional[bool] = False
    chunkName: Optional[str] = "default_chunk"

class LoggerDataBatch(BaseModel):
    data: List[LoggerDataCreate]

class LoggerDataOut(BaseModel):
    voltage: float
    current: float
    power: float
    illuminance: float
    isMaxPoint: bool
    chunkName: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True