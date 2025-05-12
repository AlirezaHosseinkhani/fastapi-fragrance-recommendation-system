# app/services/groq_recommender.py

import json
import logging
import os
from typing import Dict, Any

from dotenv import load_dotenv

from app.database import FRAGRANCE_DATABASE
from app.services.groq_service import GroqService

load_dotenv()
logger = logging.getLogger(__name__)


class GroqRecommender:
    def __init__(self, groq_service: GroqService = None):
        self.database = FRAGRANCE_DATABASE
        self.groq_service = groq_service or GroqService()

    async def analyze_personality(self, quiz_answers: Dict[str, Any]) -> str:
        """Use Groq to analyze personality based on quiz answers"""
        try:
            system_prompt = """
            You are an expert fragrance profiler who can analyze customer preferences and determine 
            their personality type. Based on their quiz answers, determine which personality type 
            best fits them from this list: playful, mysterious, elegant, bold, sensual, fresh, cozy.
            Return only the single best matching personality type without explanation.
            """

            user_prompt = f"""
            Based on these fragrance quiz answers, determine the customer's dominant personality type:

            Scent aura: {', '.join(quiz_answers.get('scent_aura', []))}
            Mood: {quiz_answers.get('mood', '')}
            Scent families: {', '.join(quiz_answers.get('scent_families', []))}
            Wear time: {quiz_answers.get('wear_time', '')}
            Season: {quiz_answers.get('season', '')}
            Feeling: {quiz_answers.get('feeling', '')}
            Inspiration: {quiz_answers.get('inspiration', '')}

            Analyze this information and return only a single word representing their 
            dominant personality: playful, mysterious, elegant, bold, sensual, fresh, or cozy.
            """

            response = self.groq_service.client.chat.completions.create(
                model=self.groq_service.model,
                messages=[
                    {"role": "system", "content": system_prompt.strip()},
                    {"role": "user", "content": user_prompt.strip()}
                ],
                temperature=float(os.getenv("LLM_TEMPERATURE", 0.3)),
                max_tokens=50
            )

            personality = response.choices[0].message.content.strip().lower()

            valid_types = ["playful", "mysterious", "elegant", "bold", "sensual", "fresh", "cozy"]
            if personality not in valid_types:
                personality = "elegant"

            return personality

        except Exception as e:
            logger.error(f"Error analyzing personality with Groq: {e}")
            return "elegant"

    async def match_fragrances(self, quiz_answers: Dict[str, Any]) -> Dict[str, Any]:
        """Use Groq to match user to main SKU and secondary SKUs based on quiz answers"""
        try:
            personality = await self.analyze_personality(quiz_answers)

            # Prepare the fragrance database in a format suitable for the prompt
            db_summary = []
            for sku_name, sku_data in self.database.items():
                summary = {
                    "name": sku_name,
                    "notes": ", ".join(sku_data["notes"]),
                    "groups": ", ".join(sku_data["groups"]),
                    "character": ", ".join(sku_data["character"]),
                    "best_for": ", ".join(sku_data["best_for"]),
                    "personality_match": ", ".join(sku_data["personality_match"])
                }
                db_summary.append(summary)

            # List of limited fragrances
            limited_fragrances = ["Ocean Rose", "Passion Orchid", "Citrus Blossom", "Moonlight Blossom"]

            system_prompt = f"""
            You are an expert fragrance consultant for Shuts By L'dora. Your job is to match customers 
            with the perfect fragrances based on their quiz answers and personality type. 
            Analyze their preferences carefully and select the best main fragrance and two complementary 
            secondary fragrances that would work well together.

            IMPORTANT RESTRICTION: From this list of fragrances: {", ".join(limited_fragrances)}, 
            include a maximum of ONE fragrance in your entire recommendation (either as main_sku OR 
            in secondary_skus, but not both) and skip them to the next offer if exist. The rest of your selections must be from next related fragrances.

            Return your recommendation as a valid JSON object with these exact fields:
            {{
                "main_sku": "Name of main fragrance",
                "secondary_skus": ["Secondary1", "Secondary2"],
                "main_notes": ["Note1", "Note2", "Note3"],
                "best_wearing_time": "When to wear it",
                "ideal_season": "Best season",
                "mood": ["Mood1", "Mood2", "Mood3"]
            }}
            """

            user_prompt = f"""
            Match this customer with the perfect fragrances:

            CUSTOMER PROFILE:
            - Personality Type: {personality}
            - Scent Aura Preferences: {', '.join(quiz_answers.get('scent_aura', []))}
            - Mood Sought: {quiz_answers.get('mood', '')}
            - Preferred Scent Families: {', '.join(quiz_answers.get('scent_families', []))}
            - Wear Time: {quiz_answers.get('wear_time', '')}
            - Preferred Season: {quiz_answers.get('season', '')}
            - Desired Feeling: {quiz_answers.get('feeling', '')}

            AVAILABLE FRAGRANCE CATALOG:
            {json.dumps(db_summary, indent=2)}

            Choose one main fragrance that best matches their personality and preferences.
            Then select two secondary fragrances that complement the main one and provide variety.

            REMEMBER: From the fragrances "Ocean Rose", "Passion Orchid", "Citrus Blossom", and "Moonlight Blossom",
            include at most ONE in your entire recommendation (either as main or secondary, not both).

            Return only a JSON object with these fields:
            - main_sku: The name of the main fragrance
            - secondary_skus: Array with exactly 2 secondary fragrance names
            - main_notes: Array with the top 3 notes from the main fragrance
            - best_wearing_time: When the main fragrance is best worn
            - ideal_season: Best season for the main fragrance
            - mood: Array with 3 character traits from the main fragrance
            """

            response = self.groq_service.client.chat.completions.create(
                model=self.groq_service.model,
                messages=[
                    {"role": "system", "content": system_prompt.strip()},
                    {"role": "user", "content": user_prompt.strip()}
                ],
                response_format={"type": "json_object"},
                temperature=float(os.getenv("LLM_TEMPERATURE", 0.3)),
                max_tokens=1024
            )

            content = response.choices[0].message.content
            recommendation = json.loads(content)

            # Validate the recommendation against limited fragrances
            limited_count = 0

            if recommendation["main_sku"] in limited_fragrances:
                limited_count += 1

            for sku in recommendation["secondary_skus"]:
                if sku in limited_fragrances:
                    limited_count += 1

            # If more than one limited fragrance is included, retry or correct
            if limited_count > 1:
                # Filter to keep at most one limited fragrance
                limited_found = False

                if recommendation["main_sku"] in limited_fragrances:
                    limited_found = True

                filtered_secondary = []
                for sku in recommendation["secondary_skus"]:
                    if sku in limited_fragrances:
                        if not limited_found:
                            filtered_secondary.append(sku)
                            limited_found = True
                        # Skip this limited fragrance as we already have one
                    else:
                        filtered_secondary.append(sku)

                # If we need to add more fragrances to get back to 2 secondary SKUs
                while len(filtered_secondary) < 2:
                    # Add a fallback fragrance not in the limited list
                    fallback_options = ["Night Light", "Rose Wood", "Amber Dusk", "Velvet Musk"]
                    for option in fallback_options:
                        if option not in filtered_secondary and option != recommendation["main_sku"]:
                            filtered_secondary.append(option)
                            break

                # Update the recommendation
                recommendation["secondary_skus"] = filtered_secondary[:2]  # Ensure exactly 2

            # Add personality to the result
            recommendation["personality"] = personality

            return recommendation

        except Exception as e:
            logger.error(f"Error matching fragrances with Groq: {e}")
            # Fall back to a basic recommendation with most popular items
            fallback = {
                "personality": "elegant",
                "main_sku": "Night Light",
                "secondary_skus": ["Rose Wood", "Amber Dusk"],
                "main_notes": ["Rosewood", "Cinnamon", "Rose"],
                "best_wearing_time": "evening",
                "ideal_season": "winter",
                "mood": ["warm", "spicy", "woody"]
            }
            return fallback

    def get_fallback_recommendation(self, personality="elegant"):
        """Return a fallback recommendation if the AI service fails"""
        # Choose a default main SKU based on personality
        personality_to_sku = {
            "playful": "Moonlit Blossom",
            "mysterious": "Agar Oud Amber",
            "elegant": "Juliet Rose",
            "bold": "Saffron Suede",
            "sensual": "Night Light",
            "fresh": "Citrus Blossom",
            "cozy": "Tonka Sage"
        }

        main_sku = personality_to_sku.get(personality, "Juliet Rose")

        complementary_skus = ["Rose Wood", "Ocean Rose"]

        # Get details from the database
        sku_data = self.database.get(main_sku, {})

        return {
            "personality": personality,
            "main_sku": main_sku,
            "secondary_skus": complementary_skus,
            "main_notes": sku_data.get("notes", [])[:3],
            "best_wearing_time": sku_data.get("best_for", ["evening"])[0],
            "ideal_season": next((s for s in sku_data.get("best_for", ["all seasons"])
                                  if s in ["spring", "summer", "fall", "winter"]), "all seasons"),
            "mood": sku_data.get("character", [])[:3]
        }
