# from app.services.storyteller import Storyteller
from fastapi import Depends
from sqlalchemy.orm import Session

from app.model.db import get_db
from app.services.groq_recommender import GroqRecommender
from app.services.groq_service import GroqService
from app.services.recommendation_tracker import RecommendationTracker
from app.services.storytelling import Storyteller


def get_recommendation_tracker(db: Session = Depends(get_db)) -> RecommendationTracker:
    return RecommendationTracker(db)


# Keep your other dependency functions the same
def get_groq_recommender() -> GroqRecommender:
    return GroqRecommender()


def get_groq_service() -> GroqService:
    return GroqService()


def get_storyteller() -> Storyteller:
    return Storyteller()
