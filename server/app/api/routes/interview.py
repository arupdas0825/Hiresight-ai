from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from app.services.career_service import CareerService

router = APIRouter()

class InterviewRequest(BaseModel):
    profile: Dict[str, Any]
    repositories: List[Dict[str, Any]]
    languages: List[Dict[str, Any]]
    target_role: str = "Full Stack Engineer"

@router.post("/")
async def generate_interview_questions(request: InterviewRequest):
    data = await CareerService.generate_interview_questions(
        request.profile, request.repositories, request.languages, request.target_role
    )
    return {"success": True, "questions": data}
