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
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:5173",  # For Vite if ever used
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(students.router)
app.include_router(skills.router)
app.include_router(analytics.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Student Skill Tracking API. Check /docs for Swagger UI."}
