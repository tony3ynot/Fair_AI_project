from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, date
from app import models, schemas


def get(db: Session, article_id: int) -> Optional[models.Article]:
    return db.query(models.Article).filter(models.Article.id == article_id).first()


def get_multi(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    source_id: Optional[int] = None
) -> List[models.Article]:
    query = db.query(models.Article)
    
    if category:
        query = query.filter(models.Article.category == category)
    if source_id:
        query = query.filter(models.Article.source_id == source_id)
    
    return query.offset(skip).limit(limit).all()


def create(db: Session, *, obj_in: schemas.ArticleCreate) -> models.Article:
    db_obj = models.Article(**obj_in.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(
    db: Session,
    *,
    db_obj: models.Article,
    obj_in: schemas.ArticleUpdate
) -> models.Article:
    update_data = obj_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj