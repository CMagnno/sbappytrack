from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
from .. import schemas, models, auth
from ..database import get_db

router = APIRouter(
    prefix="/submissions",
    tags=["submissions"],
    dependencies=[Depends(auth.get_current_user)]
)

@router.post("/", response_model=schemas.SubmissionOut)
async def submit_code(
    submission: schemas.SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    executor_url = "http://executor:8000/execute"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                executor_url,
                json={"code": submission.code, "timeout": 5},
                timeout=10.0  # Timeout para a chamada HTTP
            )
            result = response.json()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Executor service unavailable: {str(e)}"
        )
    
    db_submission = models.Submission(
        code=submission.code,
        output=result.get("output", ""),
        error=result.get("error", ""),
        time=result.get("time", 0),
        user_id=current_user.id,
        exercise_id=submission.exercise_id
    )
    
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    
    return db_submission