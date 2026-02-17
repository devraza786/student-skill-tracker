from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional

from app import database, schemas, models

router = APIRouter(
    prefix="/skills",
    tags=["Skills"]
)

@router.post("", response_model=schemas.SkillResponse, status_code=status.HTTP_201_CREATED)
def create_skill(skill: schemas.SkillCreate):
    new_skill_data = {
        "name": skill.name,
        "category": skill.category
    }
    
    try:
        response = database.supabase.table("skills").insert(new_skill_data).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create skill: {str(e)}")

    if not response.data:
        raise HTTPException(status_code=500, detail="Failed to create skill: No data returned")
    
    return response.data[0]

@router.get("", response_model=List[schemas.SkillResponse])
def get_skills(category: Optional[schemas.SkillCategory] = None):
    query = database.supabase.table("skills").select("*")
    if category:
        query = query.eq("category", category)
    
    response = query.execute()
    return response.data

@router.put("/{skill_id}", response_model=schemas.SkillResponse)
def update_skill(skill_id: int, skill_update: schemas.SkillUpdate):
    # Check if skill exists
    check = database.supabase.table("skills").select("id").eq("id", skill_id).execute()
    if not check.data:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    update_data = {}
    if skill_update.name is not None:
        update_data["name"] = skill_update.name
    if skill_update.category is not None:
        update_data["category"] = skill_update.category
    
    if update_data:
        response = database.supabase.table("skills").update(update_data).eq("id", skill_id).execute()
        if not response.data:
             raise HTTPException(status_code=500, detail="Failed to update skill")

    # Fetch updated skill
    response = database.supabase.table("skills").select("*").eq("id", skill_id).execute()
    return response.data[0]
@router.get("/{skill_id}", response_model=schemas.SkillResponse)
def get_skill(skill_id: int):
    response = database.supabase.table("skills").select("*").eq("id", skill_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Skill not found")
    return response.data[0]

@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill(skill_id: int):
    # Foreign key constraint with ON DELETE CASCADE in schema.sql will handle assignments
    response = database.supabase.table("skills").delete().eq("id", skill_id).execute()
    if not response.data:
        check = database.supabase.table("skills").select("id").eq("id", skill_id).execute()
        if not check.data:
             raise HTTPException(status_code=404, detail="Skill not found")
    return
