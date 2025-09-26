from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.v1.dependencies.db import get_db
from app import schemas, models

router = APIRouter()


@router.get("", response_model=List[schemas.NewsSource])
def read_news_sources(
    skip: int = 0,
    limit: int = 100,
    bias: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve news sources with optional filtering
    """
    query = db.query(models.NewsSource)
    
    if bias:
        query = query.filter(models.NewsSource.known_bias == bias)
    
    if is_active is not None:
        query = query.filter(models.NewsSource.is_active == is_active)
    
    return query.offset(skip).limit(limit).all()


@router.get("/{source_id}", response_model=schemas.NewsSource)
def read_news_source(
    source_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific news source by ID
    """
    source = db.query(models.NewsSource).filter(models.NewsSource.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="News source not found")
    return source