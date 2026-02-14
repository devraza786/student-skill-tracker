from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional

from app import database, schemas, models

router = APIRouter(
    prefix="/skills",
    tags=["Skills"]
)

@router.post("/", response_model=schemas.SkillResponse, status_code=status.HTTP_201_CREATED)
def create_skill(skill: schemas.SkillCreate):
    # Check for duplicate name? Not explicitly required but good practice.
    # Let's just create as requested.
    
    new_id = database.skill_id_counter
    database.skill_id_counter += 1
    
    new_skill = {
        "id": new_id,
        "name": skill.name,
        "category": skill.category
    }
    database.skills_db[new_id] = new_skill
    
    return new_skill

@router.get("/", response_model=List[schemas.SkillResponse])
def get_skills(category: Optional[schemas.SkillCategory] = None):
    if category:
        return [s for s in database.skills_db.values() if s["category"] == category]
    return list(database.skills_db.values())

@router.get("/{skill_id}", response_model=schemas.SkillResponse)
def get_skill(skill_id: int):
    if skill_id not in database.skills_db:
        raise HTTPException(status_code=404, detail="Skill not found")
    return database.skills_db[skill_id]

@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill(skill_id: int):
    if skill_id not in database.skills_db:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    del database.skills_db[skill_id]
    # Cleanup assignments?
    # Iterate over all students and remove this skill
    for s_id in database.student_skills_db:
        if skill_id in database.student_skills_db[s_id]:
            del database.student_skills_db[s_id][skill_id]
            
    return
