from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from app.services.career_service import CareerService

router = APIRouter()

class LinkedInRequest(BaseModel):
    profile: Dict[str, Any]
    repositories: List[Dict[str, Any]]
    languages: List[Dict[str, Any]]

@router.post("/")
async def optimize_linkedin(request: LinkedInRequest):
    data = await CareerService.optimize_linkedin(request.profile, request.repositories, request.languages)
    return {"success": True, "data": data}
