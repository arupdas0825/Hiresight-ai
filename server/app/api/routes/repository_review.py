from fastapi import APIRouter
from pydantic import BaseModel
from app.services.career_service import CareerService

router = APIRouter()

class RepositoryReviewRequest(BaseModel):
    repo_name: str
    language: str = ""
    stars: int = 0
    readme_content: str = ""

@router.post("/")
async def review_repository(request: RepositoryReviewRequest):
    data = await CareerService.review_repository(
        request.repo_name, request.language, request.stars, request.readme_content
    )
    return {"success": True, "data": data}
