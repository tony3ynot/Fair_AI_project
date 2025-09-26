from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime


class ArticleBase(BaseModel):
    title: str
    content: str
    author: Optional[str] = None
    published_date: datetime
    url: str
    image_url: Optional[str] = None
    summary: Optional[str] = None
    category: Optional[str] = None


class ArticleCreate(ArticleBase):
    source_id: int


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    summary: Optional[str] = None
    category: Optional[str] = None


class ArticleInDBBase(ArticleBase):
    id: int
    source_id: int
    view_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Article(ArticleInDBBase):
    pass


class ArticleInDB(ArticleInDBBase):
    pass


# For list view with bias info
class ArticleWithBias(ArticleInDBBase):
    source_name: str
    source_bias: Optional[str]
    bias_score: Optional[float]
    bias_label: Optional[str]
    confidence_score: Optional[float]