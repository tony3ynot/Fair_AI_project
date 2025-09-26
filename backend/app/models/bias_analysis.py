from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime


class BiasAnalysis(Base):
    __tablename__ = "bias_analyses"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"), unique=True, nullable=False)
    bias_score = Column(DECIMAL(3, 2), nullable=False)  # -1.00 to 1.00
    bias_label = Column(String(50), nullable=False)  # left, center-left, center, center-right, right
    confidence_score = Column(DECIMAL(3, 2), nullable=False)  # 0.00 to 1.00
    analysis_method = Column(String(100))
    key_indicators = Column(Text)  # JSON array of bias indicators
    analyzed_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    article = relationship("Article", back_populates="bias_analysis")