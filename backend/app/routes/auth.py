from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from app import database, auth_utils
from typing import Optional

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: str # 'teacher' or 'student'

class UserLogin(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
def register(user: UserRegister):
    if user.role not in ["teacher", "student"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    # Check if user exists
    check = database.supabase.table("users").select("email").eq("email", user.email).execute()
    if check.data:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth_utils.get_password_hash(user.password)
    
    new_user = {
        "email": user.email,
        "password_hash": hashed_password,
        "role": user.role
    }
    
    response = database.supabase.table("users").insert(new_user).execute()
    if not response.data:
        raise HTTPException(status_code=500, detail="Failed to register user")
    
    return {"message": "User registered successfully"}

@router.post("/login")
def login(user: UserLogin):
    response = database.supabase.table("users").select("*").eq("email", user.email).execute()
    
    if not response.data:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    db_user = response.data[0]
    
    if not auth_utils.verify_password(user.password, db_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = auth_utils.create_access_token(
        data={"sub": db_user["email"], "role": db_user["role"]}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "email": db_user["email"],
            "role": db_user["role"]
        }
    }
