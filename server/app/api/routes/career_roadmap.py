from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from app.services.career_service import CareerService

router = APIRouter()

class CareerRoadmapRequest(BaseModel):
    languages: List[Dict[str, Any]]
    target_role: str

@router.post("/")
async def generate_roadmap(request: CareerRoadmapRequest):
    data = await CareerService.generate_roadmap(request.languages, request.target_role)
    return {"success": True, "data": data}
