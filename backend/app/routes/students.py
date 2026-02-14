from fastapi import APIRouter, HTTPException, status
from typing import List

from app import database, schemas, models

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

@router.post("/", response_model=schemas.StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: schemas.StudentCreate):
    # Check for duplicate email
    for s in database.students_db.values():
        if s["email"] == student.email:
            raise HTTPException(status_code=400, detail="Email already registered")

    new_id = database.student_id_counter
    database.student_id_counter += 1

    new_student = {
        "id": new_id,
        "name": student.name,
        "email": student.email,
        "age": student.age
    }
    database.students_db[new_id] = new_student
    
    # Return formatted response
    return {
        **new_student,
        "skills": []
    }

@router.get("/", response_model=List[schemas.StudentResponse])
def get_students():
    students_list = []
    for s in database.students_db.values():
        s_id = s["id"]
        # Fetch skills for this student
        student_skills = []
        if s_id in database.student_skills_db:
            for skill_id, skill_data in database.student_skills_db[s_id].items():
                if skill_id in database.skills_db:
                    skill_info = database.skills_db[skill_id]
                    student_skills.append({
                        "skill_id": skill_id,
                        "skill_name": skill_info["name"],
                        "category": skill_info["category"],
                        "proficiency_level": skill_data["proficiency_level"],
                        "assessment_score": skill_data["assessment_score"]
                    })
        
        students_list.append({
            **s,
            "skills": student_skills
        })
    return students_list

@router.get("/{student_id}", response_model=schemas.StudentResponse)
def get_student(student_id: int):
    if student_id not in database.students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student = database.students_db[student_id]
    
    # Fetch skills
    student_skills = []
    if student_id in database.student_skills_db:
        for skill_id, skill_data in database.student_skills_db[student_id].items():
            if skill_id in database.skills_db:
                skill_info = database.skills_db[skill_id]
                student_skills.append({
                    "skill_id": skill_id,
                    "skill_name": skill_info["name"],
                    "category": skill_info["category"],
                    "proficiency_level": skill_data["proficiency_level"],
                    "assessment_score": skill_data["assessment_score"]
                })
                
    return {
        **student,
        "skills": student_skills
    }

@router.put("/{student_id}", response_model=schemas.StudentResponse)
def update_student(student_id: int, student_update: schemas.StudentUpdate):
    if student_id not in database.students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student = database.students_db[student_id]
    
    if student_update.email:
        # Check duplicate if email is changing
        if student_update.email != student["email"]:
            for s in database.students_db.values():
                if s["email"] == student_update.email:
                    raise HTTPException(status_code=400, detail="Email already registered")
        student["email"] = student_update.email
        
    if student_update.name:
        student["name"] = student_update.name
    
    if student_update.age:
        student["age"] = student_update.age
        
    database.students_db[student_id] = student
    
    # Fetch skills for response
    student_skills = []
    if student_id in database.student_skills_db:
        for skill_id, skill_data in database.student_skills_db[student_id].items():
            if skill_id in database.skills_db:
                skill_info = database.skills_db[skill_id]
                student_skills.append({
                    "skill_id": skill_id,
                    "skill_name": skill_info["name"],
                    "category": skill_info["category"],
                    "proficiency_level": skill_data["proficiency_level"],
                    "assessment_score": skill_data["assessment_score"]
                })

    return {
        **student,
        "skills": student_skills
    }

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int):
    if student_id not in database.students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    
    del database.students_db[student_id]
    if student_id in database.student_skills_db:
        del database.student_skills_db[student_id]
    return

@router.post("/{student_id}/skills", response_model=schemas.StudentSkillResponse)
def assign_skill(student_id: int, assignment: schemas.StudentSkillBase):
    if student_id not in database.students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    
    if assignment.skill_id not in database.skills_db:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    # Initialize student skills dict if not exists
    if student_id not in database.student_skills_db:
        database.student_skills_db[student_id] = {}
        
    # Check if already assigned? (Implicitly allows update or we can block)
    # prompt says "Assign skill", implies create/update.
    # Validation "Invalid assignments" might mean something else, but let's assume update is okay or new.
    
    database.student_skills_db[student_id][assignment.skill_id] = {
        "proficiency_level": assignment.proficiency_level,
        "assessment_score": assignment.assessment_score
    }
    
    skill_info = database.skills_db[assignment.skill_id]
    
    return {
        "skill_id": assignment.skill_id,
        "proficiency_level": assignment.proficiency_level,
        "assessment_score": assignment.assessment_score,
        "skill_name": skill_info["name"],
        "category": skill_info["category"]
    }
