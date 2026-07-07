from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import (
    analyze,
    upload,
    resume,
    ats,
    job_match,
    linkedin,
    portfolio,
    cover_letter,
    career_roadmap,
    interview,
    skill_gap,
    repository_review,
    assistant
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(upload.router, prefix=f"{settings.API_V1_STR}/upload", tags=["Upload"])
app.include_router(analyze.router, prefix=f"{settings.API_V1_STR}/analyze", tags=["Analysis"])
app.include_router(resume.router, prefix=f"{settings.API_V1_STR}/resume", tags=["Resume"])
app.include_router(ats.router, prefix=f"{settings.API_V1_STR}/ats", tags=["ATS"])
app.include_router(job_match.router, prefix=f"{settings.API_V1_STR}/job-match", tags=["Job Match"])
app.include_router(linkedin.router, prefix=f"{settings.API_V1_STR}/linkedin", tags=["LinkedIn"])
app.include_router(portfolio.router, prefix=f"{settings.API_V1_STR}/portfolio", tags=["Portfolio"])
app.include_router(cover_letter.router, prefix=f"{settings.API_V1_STR}/cover-letter", tags=["Cover Letter"])
app.include_router(career_roadmap.router, prefix=f"{settings.API_V1_STR}/career-roadmap", tags=["Career Roadmap"])
app.include_router(interview.router, prefix=f"{settings.API_V1_STR}/interview", tags=["Interview"])
app.include_router(skill_gap.router, prefix=f"{settings.API_V1_STR}/skill-gap", tags=["Skill Gap"])
app.include_router(repository_review.router, prefix=f"{settings.API_V1_STR}/repository-review", tags=["Repository Review"])
app.include_router(assistant.router, prefix=f"{settings.API_V1_STR}/assistant", tags=["Assistant"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": settings.PROJECT_NAME}

