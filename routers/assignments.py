from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from models import Assignment
from utils import get_current_teacher, get_db

router = APIRouter()


class AssignmentCreate(BaseModel):
    title: str
    description: str
    due_date: datetime  


@router.post("/assignments")
def create_assignment(
    data: AssignmentCreate,
    user=Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    assignment = Assignment(
        title=data.title,
        description=data.description,
        due_date=data.due_date,
        teacher_id=user.id
    )
    db.add(assignment)
    db.commit()
    return {"message": "Assignment created successfully"}

@router.get("/assignments")
def get_assignments(db: Session = Depends(get_db)):
    return db.query(Assignment).all()