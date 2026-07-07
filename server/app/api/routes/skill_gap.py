from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from app.services.career_service import CareerService

router = APIRouter()

class SkillGapRequest(BaseModel):
    languages: List[Dict[str, Any]]
    repositories: List[Dict[str, Any]] = []
    target_role: str

@router.post("/")
async def analyze_skill_gap(request: SkillGapRequest):
    data = await CareerService.analyze_skill_gap(request.languages, request.repositories, request.target_role)
    return {"success": True, "data": data}
