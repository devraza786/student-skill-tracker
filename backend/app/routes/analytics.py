from fastapi import APIRouter, HTTPException
from typing import List, Dict
from collections import Counter

from app import database, schemas

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.get("/students/{student_id}/average-proficiency")
def get_student_average_proficiency(student_id: int):
    if student_id not in database.students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    
    if student_id not in database.student_skills_db or not database.student_skills_db[student_id]:
        return {"student_id": student_id, "average_proficiency": 0.0}
    
    skills = database.student_skills_db[student_id]
    total_proficiency = sum(s["proficiency_level"] for s in skills.values())
    avg = total_proficiency / len(skills)
    
    return {"student_id": student_id, "average_proficiency": round(avg, 2)}

@router.get("/top-students")
def get_top_students():
    # Top 3 students by average assessment score
    student_scores = []
    
    for s_id, skills in database.student_skills_db.items():
        if not skills:
            continue
        
        total_score = sum(s["assessment_score"] for s in skills.values())
        avg_score = total_score / len(skills)
        student_scores.append({"student_id": s_id, "average_score": avg_score})
    
    # Sort by descending score
    student_scores.sort(key=lambda x: x["average_score"], reverse=True)
    
    top_3 = student_scores[:3]
    
    # Hydrate with student names
    result = []
    for item in top_3:
        if item["student_id"] in database.students_db:
            student = database.students_db[item["student_id"]]
            result.append({
                "student_id": item["student_id"],
                "name": student["name"],
                "average_score": round(item["average_score"], 2)
            })
            
    return result

@router.get("/most-popular-skill")
def get_most_popular_skill():
    # Skill assigned to most students
    skill_counts = Counter()
    
    for skills in database.student_skills_db.values():
        skill_counts.update(skills.keys())
        
    if not skill_counts:
        return {"message": "No skills assigned yet"}
        
    most_common = skill_counts.most_common(1)
    if not most_common:
         return {"message": "No skills assigned yet"}
         
    skill_id, count = most_common[0]
    
    if skill_id in database.skills_db:
        skill = database.skills_db[skill_id]
        return {
            "skill_id": skill_id,
            "name": skill["name"],
            "category": skill["category"],
            "student_count": count
        }
    return {"skill_id": skill_id, "student_count": count, "message": "Skill details not found"} # Should not happen

@router.get("/job-ready-students")
def get_job_ready_students():
    # At least 3 skills
    # Average assessment score > 75
    
    job_ready = []
    
    for s_id, skills in database.student_skills_db.items():
        if len(skills) < 3:
            continue
            
        total_score = sum(s["assessment_score"] for s in skills.values())
        avg_score = total_score / len(skills)
        
        if avg_score > 75:
             if s_id in database.students_db:
                student = database.students_db[s_id]
                job_ready.append({
                   "student_id": s_id,
                   "name": student["name"],
                   "email": student["email"],
                   "skill_count": len(skills),
                   "average_score": round(avg_score, 2)
                })
                
    return job_ready
