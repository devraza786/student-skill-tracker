from fastapi import APIRouter, HTTPException, status
from typing import List

from app import database, schemas, models

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

@router.post("", response_model=schemas.StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: schemas.StudentCreate):
    # Check for duplicate email
    response = database.supabase.table("students").select("*").eq("email", student.email).execute()
    if response.data:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_student_data = {
        "name": student.name,
        "email": student.email,
        "age": student.age
    }
    
    try:
        response = database.supabase.table("students").insert(new_student_data).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create student: {str(e)}")

    if not response.data:
        raise HTTPException(status_code=500, detail="Failed to create student: No data returned")
    
    created_student = response.data[0]
    
    return {
        **created_student,
        "skills": []
    }

@router.get("", response_model=List[schemas.StudentResponse])
def get_students():
    # Fetch students with their skills in one go if possible, or separately
    # Supabase supports joins via select filter
    response = database.supabase.table("students").select("*, student_skills(*, skills(*))").execute()
    
    students_list = []
    for s in response.data:
        formatted_skills = []
        for ss in s.get("student_skills", []):
            skill_info = ss.get("skills")
            if skill_info:
                formatted_skills.append({
                    "skill_id": ss["skill_id"],
                    "skill_name": skill_info["name"],
                    "category": skill_info["category"],
                    "proficiency_level": ss["proficiency_level"],
                    "assessment_score": ss["assessment_score"]
                })
        
        students_list.append({
            "id": s["id"],
            "name": s["name"],
            "email": s["email"],
            "age": s["age"],
            "skills": formatted_skills
        })
    return students_list

@router.get("/{student_id}", response_model=schemas.StudentResponse)
def get_student(student_id: int):
    response = database.supabase.table("students").select("*, student_skills(*, skills(*))").eq("id", student_id).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Student not found")
    
    s = response.data[0]
    formatted_skills = []
    for ss in s.get("student_skills", []):
        skill_info = ss.get("skills")
        if skill_info:
            formatted_skills.append({
                "skill_id": ss["skill_id"],
                "skill_name": skill_info["name"],
                "category": skill_info["category"],
                "proficiency_level": ss["proficiency_level"],
                "assessment_score": ss["assessment_score"]
            })
            
    return {
        "id": s["id"],
        "name": s["name"],
        "email": s["email"],
        "age": s["age"],
        "skills": formatted_skills
    }

@router.put("/{student_id}", response_model=schemas.StudentResponse)
def update_student(student_id: int, student_update: schemas.StudentUpdate):
    # Check if student exists
    check = database.supabase.table("students").select("id").eq("id", student_id).execute()
    if not check.data:
        raise HTTPException(status_code=404, detail="Student not found")
    
    update_data = {}
    if student_update.name is not None:
        update_data["name"] = student_update.name
    if student_update.email is not None:
        update_data["email"] = student_update.email
    if student_update.age is not None:
        update_data["age"] = student_update.age
    
    if update_data:
        response = database.supabase.table("students").update(update_data).eq("id", student_id).execute()
        if not response.data:
             raise HTTPException(status_code=500, detail="Failed to update student")

    return get_student(student_id)

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int):
    response = database.supabase.table("students").delete().eq("id", student_id).execute()
    if not response.data:
         # Check if it was because it didn't exist or just failed
         check = database.supabase.table("students").select("id").eq("id", student_id).execute()
         if not check.data:
             raise HTTPException(status_code=404, detail="Student not found")
    return

@router.post("/{student_id}/skills", response_model=schemas.StudentSkillResponse)
def assign_skill(student_id: int, assignment: schemas.StudentSkillBase):
    # Check student
    check_s = database.supabase.table("students").select("id").eq("id", student_id).execute()
    if not check_s.data:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check skill
    check_sk = database.supabase.table("skills").select("*").eq("id", assignment.skill_id).execute()
    if not check_sk.data:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    skill_info = check_sk.data[0]
    
    upsert_data = {
        "student_id": student_id,
        "skill_id": assignment.skill_id,
        "proficiency_level": assignment.proficiency_level,
        "assessment_score": assignment.assessment_score
    }
    
    response = database.supabase.table("student_skills").upsert(upsert_data).execute()
    if not response.data:
        raise HTTPException(status_code=500, detail="Failed to assign skill")
    
    return {
        "skill_id": assignment.skill_id,
        "proficiency_level": assignment.proficiency_level,
        "assessment_score": assignment.assessment_score,
        "skill_name": skill_info["name"],
        "category": skill_info["category"]
    }
