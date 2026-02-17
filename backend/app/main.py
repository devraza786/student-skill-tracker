from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import students, skills, analytics

app = FastAPI(
    title="Student Skill Tracking & Analytics API",
    description="API for managing students, skills, and tracking their progress.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
app.include_router(students.router)
app.include_router(skills.router)
app.include_router(analytics.router)
 Riverside

@app.get("/")
def read_root():
    return {"message": "Welcome to the Student Skill Tracking API. Check /docs for Swagger UI."}
