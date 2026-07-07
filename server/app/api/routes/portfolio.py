from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from app.services.career_service import CareerService

router = APIRouter()

class PortfolioRequest(BaseModel):
    portfolio_url: str = ""
    profile: Dict[str, Any]
    repositories: List[Dict[str, Any]]

@router.post("/")
async def analyze_portfolio(request: PortfolioRequest):
    data = await CareerService.analyze_portfolio(request.portfolio_url, request.profile, request.repositories)
    return {"success": True, "data": data}
