from fastapi import APIRouter
from app.api.v1.endpoints import articles, news_sources, bias_analyses

api_router = APIRouter()

api_router.include_router(articles.router, prefix="/articles", tags=["articles"])
api_router.include_router(news_sources.router, prefix="/news-sources", tags=["news sources"])
api_router.include_router(bias_analyses.router, prefix="/bias-analyses", tags=["bias analyses"])