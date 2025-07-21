from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from models import Submission, Assignment, User
from database import get_db  # Recommended way to get DB session
from utils import get_current_user  # ✅ Centralized auth logic
from schemas import SubmissionRequest

router = APIRouter()

# ✅ Submit Assignment (Students only)
@router.post("/assignments/{id}/submit")
def submit_assignment(
    id: int,
    submission: SubmissionRequest,  # ✅ Expect request body with JSON
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user.role != "student":
        raise HTTPException(status_code=403, detail="Only students can submit")

    assignment = db.query(Assignment).filter(Assignment.id == id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    new_submission = Submission(
        content=submission.content,  # ✅ Access content from request body
        assignment_id=id,
        student_id=user.id,
        submitted_at=datetime.utcnow()
    )
    db.add(new_submission)
    db.commit()
    return {"message": "Submission successful"}


# ✅ View Submissions (Teachers only)
@router.get("/assignments/{id}/submissions")
def view_submissions(
    id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can view submissions")

    assignment = db.query(Assignment).filter(Assignment.id == id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    submissions = db.query(Submission).filter(Submission.assignment_id == id).all()
    return [
        {
            "student_id": s.student_id,
            "content": s.content,
            "submitted_at": s.submitted_at
        }
        for s in submissions
    ]
