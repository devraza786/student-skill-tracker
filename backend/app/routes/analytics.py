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
    # Check student
    check_s = database.supabase.table("students").select("id").eq("id", student_id).execute()
    if not check_s.data:
        raise HTTPException(status_code=404, detail="Student not found")
    
    response = database.supabase.table("student_skills").select("proficiency_level").eq("student_id", student_id).execute()
    
    if not response.data:
        return {"student_id": student_id, "average_proficiency": 0.0}
    
    total_proficiency = sum(s["proficiency_level"] for s in response.data)
    avg = total_proficiency / len(response.data)
    
    return {"student_id": student_id, "average_proficiency": round(avg, 2)}

@router.get("/top-students")
def get_top_students():
    # Fetch all student skills joined with student names
    response = database.supabase.table("student_skills").select("student_id, assessment_score, students(name)").execute()
    
    if not response.data:
        return []
        
    student_scores = {}
    for item in response.data:
        s_id = item["student_id"]
        if s_id not in student_scores:
            student_scores[s_id] = {"total": 0, "count": 0, "name": item["students"]["name"]}
        student_scores[s_id]["total"] += item["assessment_score"]
        student_scores[s_id]["count"] += 1
    
    results = []
    for s_id, data in student_scores.items():
        results.append({
            "student_id": s_id,
            "name": data["name"],
            "average_score": round(data["total"] / data["count"], 2)
        })
        
    # Sort and take top 3
    results.sort(key=lambda x: x["average_score"], reverse=True)
    return results[:3]

@router.get("/most-popular-skill")
def get_most_popular_skill():
    # Count occurrences of each skill_id in student_skills
    response = database.supabase.table("student_skills").select("skill_id, skills(name, category)").execute()
    
    if not response.data:
        return {"message": "No skills assigned yet"}
        
    skill_counts = Counter(item["skill_id"] for item in response.data)
    most_common = skill_counts.most_common(1)
    
    if not most_common:
        return {"message": "No skills assigned yet"}
        
    skill_id, count = most_common[0]
    
    # Get skill details from the first item found with this ID
    skill_details = next(item for item in response.data if item["skill_id"] == skill_id)
    
    return {
        "skill_id": skill_id,
        "name": skill_details["skills"]["name"],
        "category": skill_details["skills"]["category"],
        "student_count": count
    }

@router.get("/job-ready-students")
def get_job_ready_students():
    # At least 3 skills
    # Average assessment score > 75
    response = database.supabase.table("student_skills").select("student_id, assessment_score, students(name, email)").execute()
    
    if not response.data:
        return []
        
    student_stats = {}
    for item in response.data:
        s_id = item["student_id"]
        if s_id not in student_stats:
            student_stats[s_id] = {"total": 0, "count": 0, "name": item["students"]["name"], "email": item["students"]["email"]}
        student_stats[s_id]["total"] += item["assessment_score"]
        student_stats[s_id]["count"] += 1
        
    job_ready = []
    for s_id, data in student_stats.items():
        avg_score = data["total"] / data["count"]
        if data["count"] >= 3 and avg_score > 75:
            job_ready.append({
                "student_id": s_id,
                "name": data["name"],
                "email": data["email"],
                "skill_count": data["count"],
                "average_score": round(avg_score, 2)
            })
            
    return job_ready
