from fastapi import APIRouter, HTTPException, Depends
from app.models.user import UserCreate, UserLogin
from app.db.mongodb import users_collection
from app.utils.password import hash_password, verify_password
from app.auth.auth import create_access_token
from bson.objectid import ObjectId

router = APIRouter(prefix="/user", tags=["User Related"])

@router.post("/register")
def register(user: UserCreate):
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists")
    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    users_collection.insert_one(user_dict)
    return {"msg": "User registered successfully"}

@router.post("/login")
def login(user: UserLogin):
    db_user = users_collection.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token}

@router.delete("/delete")
def delete_user(username: str,password: str):
    user = users_collection.find_one({"username": username})
    passwrd = users_collection.find_one({"password": password})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    users_collection.delete_one({"username": username})
    return {"msg": "User Deleted successfully"}
