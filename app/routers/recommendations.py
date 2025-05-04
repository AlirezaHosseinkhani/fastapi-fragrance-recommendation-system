# app/services/recommendation.py

from typing import Dict

from fastapi import APIRouter, Depends, HTTPException

from app.models import LanguageInput, UserInput, RecommendationResponse, RecommendationData
from app.services.fragrance_matcher import FragranceMatcher
from app.services.groq_recommender import GroqRecommender
from app.services.groq_service import GroqService
from app.services.storytelling import Storyteller

router = APIRouter(
    prefix="/api",
    tags=["recommendations"]
)


def get_groq_service():
    return GroqService()


def get_groq_recommender(groq_service: GroqService = Depends(get_groq_service)):
    return GroqRecommender(groq_service=groq_service)


def get_storyteller():
    return Storyteller()


def get_fragrance_matcher():
    return FragranceMatcher()

WELCOME_MESSAGES = {
    "English": "Welcome to Shuts By L'dora. May I ask you a few questions to begin crafting your signature blend?",
    "Persian": "به شاتس بای لدورا خوش آمدید. می‌توانم چند سوال بپرسم تا ترکیب خاص شما را بسازم؟"
}

QUIZ_QUESTIONS = {
    "English": [
        {
            "id": "scent_aura",
            "question": "Which words describe your ideal scent aura?",
            "type": "multiple",
            "options": ["Bold", "Mysterious", "Playful", "Elegant", "Seductive", "Fresh", "Warm", "Minimalist", "Exotic"],
            "max_selections": 3
        },
        {
            "id": "mood",
            "question": "What mood do you seek from your blend?",
            "type": "single",
            "options": ["Energetic and Uplifting", "Deep and Mysterious", "Cozy and Comforting", "Sophisticated and Powerful", "Free-spirited and Playful", "Romantic and Dreamy"]
        },
        {
            "id": "scent_families",
            "question": "Which scent families attract you the most?",
            "type": "multiple",
            "options": ["Fruity", "Floral", "Woody", "Spicy", "Musky", "Fresh/Green", "Sweet/Gourmand", "Resinous/Amber"],
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
            "type": "multiple",
            "options": ["Empowered", "Seductive", "Free", "Grounded", "Refreshed", "Comforted"],
            "max_selections": 2
        },
        {
            "id": "inspiration",
            "question": "Inspirational imagery or memory that comes to mind?",
            "type": "single",
            "options": [
                "A hidden rose garden at night",
                "Golden sunrise over the ocean",
                "Ancient library with leather-bound books",
                "Wild tropical jungle after rain",
                "Cozy mountain cabin with firewood scent"
            ]
        },
        # {
        #     "id": "message",
        #     "question": "Free-text message to your perfumer (optional)",
        #     "type": "text"
        # },
        # {
        #     "id": "strength",
        #     "question": "Desired strength and longevity?",
        #     "type": "single",
        #     "options": [
        #         "Subtle and skin-close",
        #         "Noticeable but not overpowering",
        #         "Bold and long-lasting",
        #         "A fragrance that evolves through the day"
        #     ]
        # }
    ],
    "Persian": [
        {
            "id": "scent_aura",
            "question": "کدام سه واژه بهترین توصیف برای شخصیت شما یا حال‌وهوایی هستند که دوست دارید عطرتان منتقل کند؟",
            "type": "multiple",
            "options": ["جسور", "رمانتیک", "مرموز", "بازیگوش", "باوقار و شیک", "خاکی و بی‌تکلف", "خلاق"],
            "max_selections": 3
        },
        {
            "id": "mood",
            "question": "دوست دارید عطرتان چه حسی را القا کند؟",
            "type": "single",
            "options": ["پرانرژی / روحیه‌بخش", "گرم و دلنشین", "اغواگر / فریبنده", "آرامش‌بخش", "بااعتمادبه‌نفس / قدرت‌بخش"]
        },
        {
            "id": "scent_families",
            "question": "کدام دسته از رایحه‌ها را بیشتر دوست دارید؟",
            "type": "multiple",
            "options": ["میوه‌ای و مرکباتی", "گلی و تازه", "چوبی و خاکی", "ادویه‌ای و شرقی", "شیرین و خوراکی (گورماند)", "سبز و گیاهی", "دریایی و ملایم (بوی رخت‌های تازه‌شسته)"],
            "max_selections": 3
        },
        {
            "id": "wear_time",
            "question": "این عطر را بیشتر در چه زمانی استفاده خواهید کرد؟",
            "type": "single",
            "options": ["روز (محیط کاری یا استفاده روزمره)", "شب / مهمانی", "همه‌کاره (در تمام طول روز)", "موقعیت‌های خاص"]
        },
        {
            "id": "season",
            "question": "حال‌وهوای کدام فصل بیشتر با سلیقه‌ شما سازگار است؟",
            "type": "single",
            "options": ["بهار (سبک و گلی)", "تابستان (درخشان و مرکباتی)", "پاییز (گرم و ادویه‌ای)", "زمستان (غنی و دودی)"]
        },
        {
            "id": "feeling",
            "question": "هنگام استفاده از این عطر، دوست دارید چه احساسی داشته باشید؟",
            "type": "multiple",
            "options": ["بااعتمادبه‌نفس", " احساسی / اغواگر", "شاد و سرحال", "آرام و ریلکس", "باطراوت و سرزنده", "راحت و آرامش‌یافته","خاص و متفاوت","قدرتمند و تأثیرگذار"],
            "max_selections": 2
        },
        {
            "id": "inspiration",
            "question": "کدام تصویر یا تجربه بیشتر با حال‌وهوای عطری که دوست دارید هماهنگ است؟",
            "type": "single",
            "options": [
                "غروب کنار دریا",
                "کلبه‌ی گرم چوبی کنار شومینه",
                "بازار پر از ادویه و رنگ",
                "باغ گل‌های شکوفه‌زده در بهار",
                "خیابان بارانی شبانه با نورهای خیس",
               "جشن شبانه‌ی پر از موسیقی و نور",
                "پیاده‌روی در جنگل مرطوب و سبز",
                "صبح آفتابی در یک مزرعه‌ی پرتقال"
            ]
        },
        # {
        #     "id": "message",
        #     "question": "پیامی برای عطرساز (اختیاری)",
        #     "type": "text"
        # },
        # {
        #     "id": "strength",
        #     "question": "میزان ماندگاری و قدرت دلخواه؟",
        #     "type": "single",
        #     "options": [
        #         "ملایم و نزدیک به پوست",
        #         "قابل‌توجه اما نه تند",
        #         "قوی و ماندگار",
        #         "عطری که در طول روز تغییر کند"
        #     ]
        # }
    ]
}



@router.post("/welcome", response_model=Dict[str, str])
async def welcome(language_input: LanguageInput):
    message = WELCOME_MESSAGES.get(language_input.language, WELCOME_MESSAGES["English"])
    return {"message": message}


@router.post("/quiz")
async def get_quiz_questions(language_input: LanguageInput):
    questions = QUIZ_QUESTIONS.get(language_input.language, QUIZ_QUESTIONS["English"])
    return {"questions": questions}

@router.post(
    "/recommend",
    response_model=RecommendationResponse,
    summary="Generate a personalized fragrance recommendation",
)
async def get_recommendation(
        user_input: UserInput,
        groq_recommender: GroqRecommender = Depends(get_groq_recommender),
        groq_service: GroqService = Depends(get_groq_service),
        storyteller: Storyteller = Depends(get_storyteller),
):
    """Generate a personalized fragrance recommendation with Groq-enhanced matching and storytelling"""
    try:
        # Convert Pydantic model to dict
        quiz_answers = user_input.quiz_answers.dict()

        # Use Groq AI to match fragrances & determine personality
        fragrance_match = await groq_recommender.match_fragrances(quiz_answers)

        # Use Groq to generate the enhanced story
        enhanced = await groq_service.enhance_story(
            user_language=user_input.language,
            user_name=user_input.name,
            personality=fragrance_match["personality"],
            fragrance_data=fragrance_match,
        )

        if enhanced and enhanced.get("status") == "success":
            # Use the Groq-generated content
            recommendation_data = enhanced["data"]
        else:
            # Fall back to the basic storyteller if Groq fails
            base_rec = storyteller.generate_story(
                user_name=user_input.name,
                personality=fragrance_match["personality"],
                fragrance_match=fragrance_match,
            )
            recommendation_data = base_rec

        recommendation_data["closing"] = storyteller.generate_closing_message()

        recommendation_data = RecommendationData(**recommendation_data)
        return RecommendationResponse(data=recommendation_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendation: {e}")


@router.post(
    "/recommend_local",
    response_model=RecommendationResponse,
    summary="Generate a personalized fragrance recommendation",
)
async def get_recommendation_local(
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
