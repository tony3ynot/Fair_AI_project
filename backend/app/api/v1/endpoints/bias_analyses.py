from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.v1.dependencies.db import get_db
from app import schemas, models

router = APIRouter()


@router.get("", response_model=List[schemas.BiasAnalysis])
def read_bias_analyses(
    skip: int = 0,
    limit: int = 100,
    bias_label: Optional[str] = None,
    min_confidence: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve bias analyses with optional filtering
    """
    query = db.query(models.BiasAnalysis)
    
    if bias_label:
        query = query.filter(models.BiasAnalysis.bias_label == bias_label)
    
    if min_confidence:
        query = query.filter(models.BiasAnalysis.confidence_score >= min_confidence)
    
    return query.offset(skip).limit(limit).all()


@router.get("/stats")
def read_bias_stats(db: Session = Depends(get_db)):
    """
    Get bias distribution statistics
    """
    bias_counts = db.query(
        models.BiasAnalysis.bias_label,
        db.func.count(models.BiasAnalysis.id).label('count')
    ).group_by(models.BiasAnalysis.bias_label).all()
    
    total_articles = db.query(models.Article).count()
    analyzed_articles = db.query(models.BiasAnalysis).count()
    
    return {
        "total_articles": total_articles,
        "analyzed_articles": analyzed_articles,
        "bias_distribution": {bias: count for bias, count in bias_counts}
    }