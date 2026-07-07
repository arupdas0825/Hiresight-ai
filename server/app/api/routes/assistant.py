from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from app.services.career_service import CareerService

router = APIRouter()

class AssistantRequest(BaseModel):
    message: str
    profile: Dict[str, Any]
    repositories: List[Dict[str, Any]] = []

@router.post("/")
async def assistant_chat(request: AssistantRequest):
    data = await CareerService.assistant_chat(request.message, request.profile, request.repositories)
    return {"success": True, "data": data}
