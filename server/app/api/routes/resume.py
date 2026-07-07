from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from app.services.career_service import CareerService

router = APIRouter()

class ResumeRequest(BaseModel):
    profile: Dict[str, Any]
    repositories: List[Dict[str, Any]]
    languages: List[Dict[str, Any]]

@router.post("/")
async def generate_resumes(request: ResumeRequest):
    data = await CareerService.generate_resumes(request.profile, request.repositories, request.languages)
    return {"success": True, "resumes": data}
