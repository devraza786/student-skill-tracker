from pydantic import BaseModel, EmailStr
from typing import List, Optional
from app.schemas import SkillCategory

# Internal models representing the data structure in our "database"
# These are similar to schemas but represent the stored state

class Student(BaseModel):
    id: int
    name: str
    email: str
    age: int

class Skill(BaseModel):
    id: int
    name: str
    category: SkillCategory

class StudentSkill(BaseModel):
    student_id: int
    skill_id: int
    proficiency_level: int
    assessment_score: int
