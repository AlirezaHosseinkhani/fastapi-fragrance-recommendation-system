import logging
from datetime import datetime
from typing import Dict, Any, List

from sqlalchemy.orm import Session

from app.model.db import Recommendation

logger = logging.getLogger(__name__)


class RecommendationTracker:
    def __init__(self, db: Session):
        self.db = db

    def add_recommendation(self, user_id: str, recommendation_data: Dict[str, Any]) -> bool:
        """Add a new recommendation to the database"""
        try:
            # Format recommendation for storage
            recommendation_entry = Recommendation(
                # user_id=user_id,
                timestamp=datetime.now(),
                main_sku=recommendation_data.get("main_sku"),
                secondary_skus=recommendation_data.get("secondary_skus", []),
                personality=recommendation_data.get("personality")
            )

            self.db.add(recommendation_entry)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error saving recommendation: {e}")
            return False

    def get_all_recommendations(self) -> List[Dict[str, Any]]:
        """Get all stored recommendations"""
        try:
            recommendations = self.db.query(Recommendation).all()
            result = []
            for rec in recommendations:
                result.append({
                    # "user_id": rec.user_id,
                    "timestamp": rec.timestamp.isoformat(),
                    "personality": rec.personality,
                    "main_sku": rec.main_sku,
                    "secondary_skus": rec.secondary_skus
                })
            return result
        except Exception as e:
            logger.error(f"Error loading recommendations: {e}")
            return []
