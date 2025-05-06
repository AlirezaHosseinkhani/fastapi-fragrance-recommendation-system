# app/services/groq_service.py
import json
import logging
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

logger = logging.getLogger(__name__)


class GroqService:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = os.getenv("LLM_MODEL_NAME", "llama3-70b-8192")

    async def enhance_story(self, user_language: str, user_name: str, personality: str, fragrance_data: dict) -> dict:
        """Generate a poetic, layered fragrance experience in the user's language"""
        try:
            main_sku = fragrance_data["main_sku"]
            secondary_skus = fragrance_data["secondary_skus"]
            main_notes = fragrance_data["main_notes"]
            best_wearing_time = fragrance_data["best_wearing_time"]
            ideal_season = fragrance_data["ideal_season"]
            mood = fragrance_data["mood"]

            system_prompt = f"""
            You are a master fragrance storyteller for Shuts By L'dora, 
            skilled in crafting poetic, emotionally resonant, and sensory-rich descriptions 
            for personalized fragrance blends. Your job is to guide the customer through their custom blend,
            offering elegant descriptions for each fragrance and two layering recipes that express their essence.
            You must respond entirely in this language: {user_language}.
            """

            user_prompt = f"""
            Create a fragrance story for {user_name}, who has a {personality} personality.

            Use these components:
            - Anchor fragrance: {main_sku}, with notes of {', '.join(main_notes)}
            - Complementary fragrances: {', '.join(secondary_skus)}
            - Best worn: {best_wearing_time}
            - Ideal season: {ideal_season}
            - Mood evoked: {', '.join(mood if isinstance(mood, list) else [mood])}

            The response must be a JSON object with these keys:
            1. greeting: A poetic introduction that celebrates their personality and invites them into the story.Begin the first paragraph explicitly with the user's name.
            Then write two or three sentences that poetically and insightfully describe the user's personality and essence, based on the answers they’ve provided.
            This introduction must establish a luxurious emotional connection and feel warm, elegant, and rich in sensory language.
            Avoid generic compliments—make each line tailored and immersive.
            2. fragrance_trio: A dictionary with three keys (anchor, mixer, accent), each describing:
                - name: the fragrance name (from the inputs)
                - description: 2--3 sentences capturing the mood and personality of each fragrance
            3. layering_recipes: A list of two blend options. Each recipe must include:
                - name: a poetic name for the blend
                - composition: {{"{main_sku}": "2 shuts", "{secondary_skus[0]}": "1 shut"}} format
                - result: a short poetic summary of the final impression this blend gives
            4. closing_line: A luxurious, elegant sentence that closes the story and makes the user feel special.

            Style must be poetic, emotional, sensory, and tailored to a {personality} personality.
            Return only valid JSON.
            """

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt.strip()},
                    {"role": "user", "content": user_prompt.strip()}
                ],
                response_format={"type": "json_object"},
                temperature=float(os.getenv("LLM_TEMPERATURE", 0.3)),
                max_tokens=1024
            )

            content = response.choices[0].message.content
            parsed = json.loads(content)

            return {
                "status": "success",
                "data": parsed
            }
        except Exception as e:
            logger.error(f"Error with Groq service: {e}")
            return {"status": "error", "message": str(e)}
