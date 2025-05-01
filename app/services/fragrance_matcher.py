from typing import Dict, Any

from app.database import FRAGRANCE_DATABASE, PERSONALITY_TONES


class FragranceMatcher:
    def __init__(self):
        self.database = FRAGRANCE_DATABASE
        self.personality_tones = PERSONALITY_TONES

    def determine_personality(self, quiz_answers: Dict[str, Any]) -> str:
        """Determine the dominant personality type based on quiz answers"""
        # Map quiz answers to personality traits
        personality_map = {
            "playful": 0,
            "mysterious": 0,
            "elegant": 0,
            "bold": 0,
            "sensual": 0,
            "fresh": 0,
            "cozy": 0
        }

        # Analyze scent aura
        for word in quiz_answers.get("scent_aura", []):
            if word.lower() in ["playful", "fresh", "free-spirited"]:
                personality_map["playful"] += 2
                personality_map["fresh"] += 1
            elif word.lower() in ["mysterious", "sophisticated"]:
                personality_map["mysterious"] += 2
                personality_map["elegant"] += 1
            elif word.lower() in ["elegant", "romantic"]:
                personality_map["elegant"] += 2
            elif word.lower() in ["bold", "seductive"]:
                personality_map["bold"] += 1
                personality_map["sensual"] += 1
            elif word.lower() in ["warm", "minimalist"]:
                personality_map["cozy"] += 1
                personality_map["fresh"] += 1
            elif word.lower() in ["exotic", "seductive"]:
                personality_map["sensual"] += 2

        # Analyze mood
        mood = quiz_answers.get("mood", "").lower()
        if mood in ["energetic and uplifting"]:
            personality_map["playful"] += 2
            personality_map["fresh"] += 1
        elif mood in ["deep and mysterious"]:
            personality_map["mysterious"] += 2
        elif mood in ["cozy and comforting"]:
            personality_map["cozy"] += 2
        elif mood in ["sophisticated and powerful"]:
            personality_map["elegant"] += 1
            personality_map["bold"] += 1
        elif mood in ["romantic and dreamy"]:
            personality_map["elegant"] += 1
            personality_map["sensual"] += 1
        elif mood in ["free-spirited and playful"]:
            personality_map["playful"] += 2

        # Analyze feeling
        feeling = quiz_answers.get("feeling", "").lower()
        if feeling in ["empowered"]:
            personality_map["bold"] += 2
        elif feeling in ["seductive"]:
            personality_map["sensual"] += 2
        elif feeling in ["free"]:
            personality_map["playful"] += 1
            personality_map["fresh"] += 1
        elif feeling in ["grounded"]:
            personality_map["cozy"] += 1
        elif feeling in ["refreshed"]:
            personality_map["fresh"] += 2
        elif feeling in ["comforted"]:
            personality_map["cozy"] += 2

        # Find highest personality score
        dominant_personality = max(personality_map.items(), key=lambda x: x[1])[0]
        return dominant_personality

    def match_fragrances(self, quiz_answers: Dict[str, Any]) -> Dict[str, Any]:
        """Match user to main SKU and secondary SKUs based on quiz answers"""
        personality = self.determine_personality(quiz_answers)

        # Score each fragrance for this user
        fragrance_scores = {}
        for sku_name, sku_data in self.database.items():
            score = 0

            # Match by personality
            for match in sku_data["personality_match"]:
                if match == personality:
                    score += 3
                elif match in quiz_answers.get("scent_aura", []):
                    score += 2

            # Match by scent families
            for family in quiz_answers.get("scent_families", []):
                family_lower = family.lower()
                for group in sku_data["groups"]:
                    if family_lower in group.lower():
                        score += 2

            # Match by season
            season = quiz_answers.get("season", "").lower()
            for best_time in sku_data["best_for"]:
                if season in best_time.lower():
                    score += 1

            # Match by wear time
            wear_time = quiz_answers.get("wear_time", "").lower()
            for best_time in sku_data["best_for"]:
                if wear_time in best_time.lower():
                    score += 1

            fragrance_scores[sku_name] = score

        # Sort by score and get top fragrances
        sorted_fragrances = sorted(fragrance_scores.items(), key=lambda x: x[1], reverse=True)

        # Get main SKU and 2 secondary SKUs
        main_sku = sorted_fragrances[0][0]

        # Make sure secondary SKUs are different from main SKU
        # and complement it based on character differences
        secondary_skus = []

        # Get main SKU character
        main_character = set(self.database[main_sku]["character"])

        # Find complementary SKUs (different character but still high score)
        for sku_name, score in sorted_fragrances[1:]:
            sku_character = set(self.database[sku_name]["character"])
            # If characters are different enough, it's a good complement
            if len(main_character.intersection(sku_character)) < 2:
                secondary_skus.append(sku_name)
                if len(secondary_skus) == 2:
                    break

        # If we don't have 2 secondary SKUs yet, just take the next highest scored SKUs
        remaining_needed = 2 - len(secondary_skus)
        if remaining_needed > 0:
            for sku_name, score in sorted_fragrances[1:]:
                if sku_name not in secondary_skus:
                    secondary_skus.append(sku_name)
                    if len(secondary_skus) == 2:
                        break

        # Create the blend recommendation
        result = {
            "personality": personality,
            "main_sku": main_sku,
            "secondary_skus": secondary_skus,
            "main_notes": self.database[main_sku]["notes"][:3],  # Top 3 notes
            "best_wearing_time": self.database[main_sku]["best_for"][0],
            "ideal_season": next((season for season in self.database[main_sku]["best_for"] if
                                  season in ["spring", "summer", "fall", "winter"]), "all seasons"),
            "mood": self.database[main_sku]["character"][:3]  # Top 3 character traits
        }

        return result
