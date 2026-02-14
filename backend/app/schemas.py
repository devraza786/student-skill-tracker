from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional
from enum import Enum

class SkillCategory(str, Enum):
    FRONTEND = "Frontend"
    BACKEND = "Backend"
    DEVOPS = "DevOps"
    AI = "AI"

# --- Skill Schemas ---
class SkillBase(BaseModel):
    name: str = Field(..., min_length=1, description="Name of the skill")
    category: SkillCategory

class SkillCreate(SkillBase):
    pass

class SkillResponse(SkillBase):
    id: int

    class Config:
        from_attributes = True

# --- Student Skill Association Schemas ---
class StudentSkillBase(BaseModel):
    skill_id: int
    proficiency_level: int = Field(..., ge=1, le=5, description="Proficiency level (1-5)")
    assessment_score: int = Field(..., ge=0, le=100, description="Assessment score (0-100)")

class StudentSkillCreate(StudentSkillBase):
    pass

class StudentSkillResponse(StudentSkillBase):
    skill_name: str
    category: SkillCategory

# --- Student Schemas ---
class StudentBase(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    age: int = Field(..., gt=15, description="Age must be greater than 15")

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int
    skills: List[StudentSkillResponse] = []

    class Config:
        from_attributes = True

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, gt=15)
