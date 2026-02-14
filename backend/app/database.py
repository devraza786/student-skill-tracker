from typing import Dict, List

# In-memory storage
# Students: id -> Student data
students_db: Dict[int, Dict] = {}

# Skills: id -> Skill data
skills_db: Dict[int, Dict] = {}

# Student Skills: student_id -> {skill_id -> alignment data}
student_skills_db: Dict[int, Dict[int, Dict]] = {}

# Counters for auto-incrementing IDs
student_id_counter = 1
skill_id_counter = 1
