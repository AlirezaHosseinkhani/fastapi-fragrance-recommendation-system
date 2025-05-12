# app/services/recommendation_tracker.py

import json
import logging
import os
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)


class RecommendationTracker:
    def __init__(self, file_path="recommendations_history.json"):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create recommendations file if it doesn't exist"""
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)

    def add_recommendation(self, user_id: str, recommendation_data: Dict[str, Any]):
        """Add a new recommendation to the tracking file"""
        try:
            # Load existing recommendations
            with open(self.file_path, 'r') as f:
                recommendations = json.load(f)

            # Format recommendation for storage
            timestamp = datetime.now().isoformat()
            recommendation_entry = {
                # "user_id": user_id,
                "timestamp": timestamp,
                "main_sku": recommendation_data.get("main_sku"),
                "secondary_skus": recommendation_data.get("secondary_skus", []),
                "personality": recommendation_data.get("personality")
            }

            recommendations.append(recommendation_entry)

            with open(self.file_path, 'w') as f:
                json.dump(recommendations, f, indent=2)

            return True
        except Exception as e:
            logger.error(f"Error saving recommendation: {e}")
            return False

    def get_all_recommendations(self):
        """Get all stored recommendations"""
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading recommendations: {e}")
            return []
