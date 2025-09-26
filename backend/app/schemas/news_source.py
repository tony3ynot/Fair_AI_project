from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NewsSourceBase(BaseModel):
    name: str
    domain: str
    description: Optional[str] = None
    known_bias: Optional[str] = None
    country: str = "KR"
    language: str = "ko"
    is_active: bool = True


class NewsSourceCreate(NewsSourceBase):
    pass


class NewsSourceUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    description: Optional[str] = None
    known_bias: Optional[str] = None
    is_active: Optional[bool] = None


class NewsSourceInDBBase(NewsSourceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NewsSource(NewsSourceInDBBase):
    pass


class NewsSourceInDB(NewsSourceInDBBase):
    pass