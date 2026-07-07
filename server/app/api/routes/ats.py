from fastapi import APIRouter
from pydantic import BaseModel
from app.services.career_service import CareerService

router = APIRouter()

class ATSRequest(BaseModel):
    resume_text: str
    job_description: str

@router.post("/")
async def analyze_ats(request: ATSRequest):
    data = await CareerService.analyze_ats(request.resume_text, request.job_description)
    return {"success": True, "data": data}
