from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.db.mongodb import tasks_collection
from app.models.task import TaskCreate
from app.auth.auth import verify_token
from bson.objectid import ObjectId
from datetime import datetime
from zoneinfo import ZoneInfo

router = APIRouter(prefix="/tasks", tags=["Tasks Related"])
security = HTTPBearer()  # Enables Authorize button in Swagger UI

# Get current user from JWT token
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=403, detail="Invalid or expired token")
    return payload["sub"]

# Convert ObjectId to string and clean up MongoDB response
def convert_objectid(doc: dict) -> dict:
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

# Create a new task
@router.post("/")
def create_task(task: TaskCreate, username: str = Depends(get_current_user)):
    task_doc = {
        "name": task.name,
        "due_date": task.due_date,
        "created_at": datetime.now(ZoneInfo("Asia/Kolkata")),
        "completed": "pending",
        "owner": username
    }
    result = tasks_collection.insert_one(task_doc)
    return {"id": str(result.inserted_id)}

# List all tasks for the current user
@router.get("/")
def list_tasks(username: str = Depends(get_current_user)):
    tasks = tasks_collection.find({"owner": username})
    return [convert_objectid(task) for task in tasks]

# Delete a task (if it belongs to the current user)
@router.delete("/")
def delete_task(task_id: str, username: str = Depends(get_current_user)):
    result = tasks_collection.delete_one({"_id": ObjectId(task_id), "owner": username})
    if result.deleted_count == 1:
        return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")

@router.put("/")
def mark_done(task_id: str):
    result = tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": {"completed": "done"}})
    if result.modified_count:
        return {"message": "Task marked as done"}
    raise HTTPException(status_code=404, detail="Task not found")