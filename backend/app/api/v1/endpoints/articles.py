from fastapi import APIRouter, Depends, HTTPException, Query, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.api.v1.dependencies.db import get_db
from app import schemas, models
from app.crud import article as article_crud
from datetime import datetime, date
import json

router = APIRouter()


@router.get("", response_model=List[schemas.ArticleWithBias])
def read_articles(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    bias_label: Optional[str] = None,
    source_id: Optional[int] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve articles with optional filtering
    """
    query = db.query(models.Article).join(models.NewsSource).outerjoin(models.BiasAnalysis)
    
    if category:
        query = query.filter(models.Article.category == category)
    
    if bias_label:
        query = query.filter(models.BiasAnalysis.bias_label == bias_label)
    
    if source_id:
        query = query.filter(models.Article.source_id == source_id)
    
    if date_from:
        query = query.filter(models.Article.published_date >= date_from)
    
    if date_to:
        query = query.filter(models.Article.published_date <= date_to)
    
    articles = query.order_by(models.Article.published_date.desc()).offset(skip).limit(limit).all()
    
    # Format response with bias info
    result = []
    for article in articles:
        article_data = {
            **article.__dict__,
            "source_name": article.source.name,
            "source_bias": article.source.known_bias,
            "bias_score": article.bias_analysis.bias_score if article.bias_analysis else None,
            "bias_label": article.bias_analysis.bias_label if article.bias_analysis else None,
            "confidence_score": article.bias_analysis.confidence_score if article.bias_analysis else None,
        }
        result.append(schemas.ArticleWithBias(**article_data))
    
    return result


@router.get("/{article_id}", response_model=schemas.ArticleWithBias)
def read_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific article by ID with bias analysis
    """
    article = db.query(models.Article).options(
        joinedload(models.Article.source),
        joinedload(models.Article.bias_analysis)
    ).filter(models.Article.id == article_id).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Increment view count
    article.view_count += 1
    db.commit()
    db.refresh(article)
    
    # Create proper dict without SQLAlchemy internal attributes
    article_dict = {
        "id": article.id,
        "source_id": article.source_id,
        "title": article.title,
        "content": article.content,
        "author": article.author,
        "published_date": article.published_date,
        "url": article.url,
        "image_url": article.image_url,
        "summary": article.summary,
        "category": article.category,
        "view_count": article.view_count,
        "created_at": article.created_at,
        "updated_at": article.updated_at,
        "source_name": article.source.name,
        "source_bias": article.source.known_bias,
        "bias_score": article.bias_analysis.bias_score if article.bias_analysis else None,
        "bias_label": article.bias_analysis.bias_label if article.bias_analysis else None,
        "confidence_score": article.bias_analysis.confidence_score if article.bias_analysis else None,
    }
    
    return schemas.ArticleWithBias(**article_dict)


@router.get("/{article_id}/related", response_model=List[schemas.ArticleWithBias])
def read_related_articles(
    article_id: int,
    relation_type: Optional[str] = None,
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """
    Get related articles for a specific article
    """
    query = db.query(models.Article).join(
        models.RelatedArticle, 
        models.Article.id == models.RelatedArticle.related_article_id
    ).filter(
        models.RelatedArticle.article_id == article_id
    )
    
    if relation_type:
        query = query.filter(models.RelatedArticle.relation_type == relation_type)
    
    query = query.order_by(models.RelatedArticle.similarity_score.desc())
    
    related_articles = query.options(
        joinedload(models.Article.source),
        joinedload(models.Article.bias_analysis)
    ).limit(limit).all()
    
    result = []
    for article in related_articles:
        article_dict = {
            "id": article.id,
            "source_id": article.source_id,
            "title": article.title,
            "content": article.content,
            "author": article.author,
            "published_date": article.published_date,
            "url": article.url,
            "image_url": article.image_url,
            "summary": article.summary,
            "category": article.category,
            "view_count": article.view_count,
            "created_at": article.created_at,
            "updated_at": article.updated_at,
            "source_name": article.source.name,
            "source_bias": article.source.known_bias,
            "bias_score": article.bias_analysis.bias_score if article.bias_analysis else None,
            "bias_label": article.bias_analysis.bias_label if article.bias_analysis else None,
            "confidence_score": article.bias_analysis.confidence_score if article.bias_analysis else None,
        }
        result.append(schemas.ArticleWithBias(**article_dict))
    
    return result