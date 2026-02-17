from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import students, skills, analytics, auth

app = FastAPI(
    title="Student Skill Tracking & Analytics API",
    description="API for managing students, skills, and tracking their progress.",
    version="1.0.0"
)

# Disable strict slashes globally
app.router.redirect_slashes = False

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(students.router)
app.include_router(skills.router)
app.include_router(analytics.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Student Skill Tracking API. Check /docs for Swagger UI."}
