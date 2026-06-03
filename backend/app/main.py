from fastapi import FastAPI

from app.core.database import Base, engine

from app.models.user import User

from app.api.routes.auth import router as auth_router

from app.models.resume import Resume

from app.api.routes.resume import router as resume_router

from app.api.routes.ats import (
    router as ats_router
)


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI()


# Register routes
app.include_router(auth_router)

# Resume upload Routes
app.include_router(resume_router)

# ATS Router
app.include_router(ats_router)


@app.get("/")
def root():
    return {
        "message": "API is running"
    }