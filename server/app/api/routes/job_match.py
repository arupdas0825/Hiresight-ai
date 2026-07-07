from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from app.services.career_service import CareerService

router = APIRouter()

class JobMatchRequest(BaseModel):
    resume_text: str
    job_description: str
    repositories: List[Dict[str, Any]] = []

@router.post("/")
async def match_job(request: JobMatchRequest):
    data = await CareerService.match_job(request.resume_text, request.job_description, request.repositories)
    return {"success": True, "data": data}
