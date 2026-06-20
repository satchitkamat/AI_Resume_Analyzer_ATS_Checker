from fastapi import FastAPI

from app.core.database import Base, engine

from app.api.routes.auth import router as auth_router

from app.api.routes.resume import router as resume_router

from app.api.routes.ats import router as ats_router

from app.api.routes.dashboard import router as dashboard_router

from app.api.routes.candidate_ranking import router as candidateRanking_router

from app.api.routes.candidate_search import router as candidateSearch_router

from app.api.routes.pipeline import (
    router as pipeline_router
)

from app.api.routes.bulk_screening import router as bulk_screening_router



# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI()


# Register routes
app.include_router(auth_router)

# Resume upload Routes
app.include_router(resume_router)

# ATS Router
app.include_router(ats_router)

# Candidate Ranking Router
app.include_router(candidateRanking_router)

# Dashboard Router
app.include_router(dashboard_router)

# Candidate Search Router
app.include_router(candidateSearch_router)

# Pipeline Route
app.include_router(
    pipeline_router
)

# Bulk Screening
app.include_router(
    bulk_screening_router
)

@app.get("/")
def root():
    return {
        "message": "API is running"
    }