from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("news_sources.id"), nullable=False)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String(255))
    published_date = Column(DateTime, nullable=False)
    url = Column(String(1000), unique=True, nullable=False)
    image_url = Column(String(1000))
    summary = Column(Text)
    category = Column(String(100))
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    source = relationship("NewsSource", back_populates="articles")
    bias_analysis = relationship("BiasAnalysis", back_populates="article", uselist=False)
    related_articles = relationship("RelatedArticle", foreign_keys="RelatedArticle.article_id", back_populates="article")
    related_to = relationship("RelatedArticle", foreign_keys="RelatedArticle.related_article_id", back_populates="related_article")