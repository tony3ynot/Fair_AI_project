from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime


class RelatedArticle(Base):
    __tablename__ = "related_articles"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    related_article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    relation_type = Column(String(50))  # same_topic, different_perspective, follow_up
    similarity_score = Column(DECIMAL(3, 2))  # 0.00 to 1.00
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    article = relationship("Article", foreign_keys=[article_id], back_populates="related_articles")
    related_article = relationship("Article", foreign_keys=[related_article_id], back_populates="related_to")
    
    __table_args__ = (
        UniqueConstraint('article_id', 'related_article_id', name='unique_relation'),
    )