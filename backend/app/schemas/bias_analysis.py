from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class BiasAnalysisBase(BaseModel):
    bias_score: float = Field(..., ge=-1.0, le=1.0)
    bias_label: str
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    analysis_method: Optional[str] = None
    key_indicators: Optional[List[str]] = None


class BiasAnalysisCreate(BiasAnalysisBase):
    article_id: int


class BiasAnalysisUpdate(BaseModel):
    bias_score: Optional[float] = Field(None, ge=-1.0, le=1.0)
    bias_label: Optional[str] = None
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    analysis_method: Optional[str] = None
    key_indicators: Optional[List[str]] = None


class BiasAnalysisInDBBase(BiasAnalysisBase):
    id: int
    article_id: int
    analyzed_at: datetime

    class Config:
        from_attributes = True


class BiasAnalysis(BiasAnalysisInDBBase):
    pass


class BiasAnalysisInDB(BiasAnalysisInDBBase):
    pass