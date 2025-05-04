from typing import List, Optional, Dict

from pydantic import BaseModel, Field


class QuizAnswer(BaseModel):
    scent_aura: List[str] = Field(..., description="Words describing ideal scent aura")
    mood: str = Field(..., description="Mood sought from the blend")
    scent_families: List[str] = Field(..., description="Preferred scent families")
    wear_time: str = Field(..., description="When the scent will be worn")
    season: str = Field(..., description="Preferred season or climate")
    # feeling: str = Field(..., description="How user wants to feel when wearing it")
    feeling: List[str] = Field(..., description="How user wants to feel when wearing it")
    inspiration: Optional[str] = Field(..., description="Inspirational imagery or memory")
    message: Optional[str] = Field(None, description="Free-text message to perfumer")
    strength: Optional[str] = Field(..., description="Desired strength and longevity")


class LanguageInput(BaseModel):
    language: str = Field(..., description="User's language")

class UserInput(BaseModel):
    language: str = Field(..., description="User's language")
    name: str = Field(..., description="User's first name")
    quiz_answers: QuizAnswer


class FragranceDetails(BaseModel):
    """Model for a fragrance's description and characteristics"""
    name: str
    description: str


class BlendRecipe(BaseModel):
    """Model for a blend recipe with a name, composition, and result"""
    name: str
    composition: Dict[str, str]
    result: str


class FragranceTrio(BaseModel):
    """Model for the trio of fragrances in the personalized blend"""
    anchor: FragranceDetails
    mixer: FragranceDetails
    accent: FragranceDetails


class RecommendationData(BaseModel):
    """Model for the full recommendation data returned to the user"""
    greeting: str
    fragrance_trio: FragranceTrio
    layering_recipes: List[BlendRecipe]
    closing_line: Optional[str] = None


class RecommendationResponse(BaseModel):
    """Response model for the recommendation endpoint"""
    status: str = "success"
    data: RecommendationData
