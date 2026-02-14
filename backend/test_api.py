import requests
import time
import sys

BASE_URL = "http://127.0.0.1:8000"

def wait_for_server():
    for _ in range(10):
        try:
            response = requests.get(BASE_URL)
            if response.status_code == 200:
                print("Server is up!")
                return True
        except requests.exceptions.ConnectionError:
            time.sleep(1)
            print("Waiting for server...")
    return False

def test_students_crud():
    print("\n--- Testing Student CRUD ---")
    # Create Student
    student_data = {
        "name": "Alice Smith",
        "email": "alice@example.com",
        "age": 20
    }
    response = requests.post(f"{BASE_URL}/students/", json=student_data)
    assert response.status_code == 201
    student_id = response.json()["id"]
    print(f"Created student with ID: {student_id}")

    # Get Student
    response = requests.get(f"{BASE_URL}/students/{student_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Alice Smith"
    print("Fetched student successfully")

    # Update Student
    update_data = {"age": 21}
    response = requests.put(f"{BASE_URL}/students/{student_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["age"] == 21
    print("Updated student successfully")
    
    return student_id

def test_skills_crud():
    print("\n--- Testing Skill CRUD ---")
    # Create Skills
    skills = [
        {"name": "Python", "category": "Backend"},
        {"name": "React", "category": "Frontend"},
        {"name": "Docker", "category": "DevOps"},
        {"name": "Machine Learning", "category": "AI"}
    ]
    created_skills = []
    for s in skills:
        response = requests.post(f"{BASE_URL}/skills/", json=s)
        assert response.status_code == 201
        created_skills.append(response.json())
        print(f"Created skill: {s['name']}")
        
    return created_skills

def test_assignments_and_analytics(student_id, skills):
    print("\n--- Testing Assignments & Analytics ---")
    # Assign skills to Alice
    # Python: Prof 4, Score 85
    requests.post(f"{BASE_URL}/students/{student_id}/skills", json={
        "skill_id": skills[0]["id"],
        "proficiency_level": 4,
        "assessment_score": 85
    })
    
    # React: Prof 3, Score 70
    requests.post(f"{BASE_URL}/students/{student_id}/skills", json={
        "skill_id": skills[1]["id"],
        "proficiency_level": 3,
        "assessment_score": 70
    })
    
    # Create another student Bob
    bob = requests.post(f"{BASE_URL}/students/", json={
        "name": "Bob Jones",
        "email": "bob@example.com",
        "age": 22
    }).json()
    
    # Assign Python to Bob: Prof 5, Score 95
    requests.post(f"{BASE_URL}/students/{bob['id']}/skills", json={
        "skill_id": skills[0]["id"],
        "proficiency_level": 5,
        "assessment_score": 95
    })
    
    # Assign Docker to Bob: Prof 2, Score 60
    requests.post(f"{BASE_URL}/students/{bob['id']}/skills", json={
        "skill_id": skills[2]["id"],
        "proficiency_level": 2,
        "assessment_score": 60
    })

    # Create Charlie (Job Ready)
    charlie = requests.post(f"{BASE_URL}/students/", json={
        "name": "Charlie Day",
        "email": "charlie@example.com",
        "age": 25
    }).json()
    
    requests.post(f"{BASE_URL}/students/{charlie['id']}/skills", json={"skill_id": skills[0]["id"], "proficiency_level": 5, "assessment_score": 90}) # Python
    requests.post(f"{BASE_URL}/students/{charlie['id']}/skills", json={"skill_id": skills[1]["id"], "proficiency_level": 4, "assessment_score": 80}) # React
    requests.post(f"{BASE_URL}/students/{charlie['id']}/skills", json={"skill_id": skills[2]["id"], "proficiency_level": 4, "assessment_score": 85}) # Docker

    # --- Analytics Tests ---
    
    # 1. Average Proficiency for Bob
    # (5 + 2) / 2 = 3.5
    response = requests.get(f"{BASE_URL}/analytics/students/{bob['id']}/average-proficiency")
    assert response.status_code == 200
    print(f"Bob's Avg Proficiency: {response.json()['average_proficiency']} (Expected 3.5)")
    assert response.json()['average_proficiency'] == 3.5
    
    # 2. Most Popular Skill
    # Python (3 students), React (2), Docker (2)
    response = requests.get(f"{BASE_URL}/analytics/most-popular-skill")
    assert response.status_code == 200
    print(f"Most Popular Skill: {response.json()['name']} with {response.json()['student_count']} students")
    assert response.json()['name'] == "Python"
    
    # 3. Top Students
    # Alice: (85+70)/2 = 77.5
    # Bob: (95+60)/2 = 77.5
    # Charlie: (90+80+85)/3 = 85.0
    response = requests.get(f"{BASE_URL}/analytics/top-students")
    assert response.status_code == 200
    top = response.json()
    print("Top Students:", top)
    assert top[0]['name'] == "Charlie Day"
    
    # 4. Job Ready
    # Charlie has 3 skills and avg > 75
    response = requests.get(f"{BASE_URL}/analytics/job-ready-students")
    assert response.status_code == 200
    job_ready = response.json()
    print("Job Ready Students:", [s['name'] for s in job_ready])
    assert len(job_ready) == 1
    assert job_ready[0]['name'] == "Charlie Day"

if __name__ == "__main__":
    if not wait_for_server():
        print("Server could not be reached.")
        sys.exit(1)
        
    try:
        s_id = test_students_crud()
        skills = test_skills_crud()
        test_assignments_and_analytics(s_id, skills)
        print("\nAll tests passed!")
    except Exception as e:
        print(f"\nTests failed: {e}")
        sys.exit(1)
