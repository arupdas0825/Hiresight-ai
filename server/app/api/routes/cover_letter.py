from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from app.services.career_service import CareerService

router = APIRouter()

class CoverLetterRequest(BaseModel):
    company: str
    role: str
    description: str
    letter_type: str
    profile: Dict[str, Any]
    languages: List[Dict[str, Any]]

@router.post("/")
async def generate_cover_letter(request: CoverLetterRequest):
    data = await CareerService.generate_cover_letter(
        request.company, request.role, request.description, request.letter_type, request.profile, request.languages
    )
    return {"success": True, "data": data}
