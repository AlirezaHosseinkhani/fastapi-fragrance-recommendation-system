from typing import Dict

from fastapi import APIRouter, Depends, HTTPException

from app.models import UserInput, RecommendationResponse, RecommendationData
from app.services.fragrance_matcher import FragranceMatcher
from app.services.groq_service import GroqService
from app.services.storytelling import Storyteller

router = APIRouter(
    prefix="/api",
    tags=["recommendations"]
)


def get_fragrance_matcher():
    return FragranceMatcher()


def get_storyteller():
    return Storyteller()


def get_groq_service():
    return GroqService()


@router.get("/welcome", response_model=Dict[str, str])
async def welcome():
    return {
        "message": "Welcome to Shuts By L'dora. May I ask you a few questions to begin crafting your signature blend?"
    }


@router.get("/quiz")
async def get_quiz_questions():
    return {
        "questions": [
            {
                "id": "scent_aura",
                "question": "Which words describe your ideal scent aura?",
                "type": "multiple",
                "options": ["Bold", "Mysterious", "Playful", "Elegant", "Seductive", "Fresh", "Warm", "Minimalist",
                            "Exotic"],
                "max_selections": 3
            },
            {
                "id": "mood",
                "question": "What mood do you seek from your blend?",
                "type": "single",
                "options": ["Energetic and Uplifting", "Deep and Mysterious", "Cozy and Comforting",
                            "Sophisticated and Powerful", "Free-spirited and Playful", "Romantic and Dreamy"]
            },
            {
                "id": "scent_families",
                "question": "Which scent families attract you the most?",
                "type": "multiple",
                "options": ["Fruity", "Floral", "Woody", "Spicy", "Musky", "Fresh/Green", "Sweet/Gourmand",
                            "Resinous/Amber"],
                "max_selections": 3
            },
            {
                "id": "wear_time",
                "question": "When will you mostly wear this scent?",
                "type": "single",
                "options": ["Morning", "Afternoon", "Evening/Night", "All day", "Special Occasions"]
            },
            {
                "id": "season",
                "question": "Preferred season or climate?",
                "type": "single",
                "options": ["Spring", "Summer", "Fall", "Winter", "Tropical / Hot", "Cool / Crisp"]
            },
            {
                "id": "feeling",
                "question": "How do you want to feel when wearing it?",
                "type": "single",
                "options": ["Empowered", "Seductive", "Free", "Grounded", "Refreshed", "Comforted"]
            },
            {
                "id": "inspiration",
                "question": "Inspirational imagery or memory that comes to mind?",
                "type": "single",
                "options": ["A hidden rose garden at night", "Golden sunrise over the ocean",
                            "Ancient library with leather-bound books", "Wild tropical jungle after rain",
                            "Cozy mountain cabin with firewood scent"]
            },
            {
                "id": "message",
                "question": "Free-text message to your perfumer (optional)",
                "type": "text"
            },
            {
                "id": "strength",
                "question": "Desired strength and longevity?",
                "type": "single",
                "options": ["Subtle and skin-close", "Noticeable but not overpowering",
                            "Bold and long-lasting", "A fragrance that evolves through the day"]
            }
        ]
    }


@router.post(
    "/recommend",
    response_model=RecommendationResponse,
    summary="Generate a personalized fragrance recommendation",
)
async def get_recommendation(
        user_input: UserInput,
        fragrance_matcher: FragranceMatcher = Depends(get_fragrance_matcher),
        storyteller: Storyteller = Depends(get_storyteller),
        groq_service: GroqService = Depends(get_groq_service),
):
    """Generate a personalized fragrance recommendation with Groq-enhanced storytelling"""
    try:
        # Convert Pydantic model to dict
        quiz_answers = user_input.quiz_answers.dict()

        # Match fragrances & determine personality
        fragrance_match = fragrance_matcher.match_fragrances(quiz_answers)
        personality = fragrance_matcher.determine_personality(quiz_answers)

        # Try to generate with Groq first
        enhanced = await groq_service.enhance_story(
            user_language=user_input.language,
            user_name=user_input.name,
            personality=personality,
            fragrance_data=fragrance_match,
        )

        if enhanced and enhanced.get("status") == "success":
            # Use the Groq-generated content
            recommendation_data = enhanced["data"]
        else:
            # Fall back to the basic storyteller if Groq fails
            base_rec = storyteller.generate_story(
                user_name=user_input.name,
                personality=personality,
                fragrance_match=fragrance_match,
            )
            recommendation_data = base_rec

        recommendation_data["closing"] = storyteller.generate_closing_message()

        recommendation_data = RecommendationData(**recommendation_data)
        return RecommendationResponse(data=recommendation_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendation: {e}")
