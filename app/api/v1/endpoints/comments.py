from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.api.v1.endpoints.users import get_current_user
from app.models.user import User
from app.models.comment import Comment
from app.models.task import Task
from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse

router = APIRouter(prefix="/comments", tags=["comments"])

@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == comment_data.task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    new_comment = Comment(
        task_id=comment_data.task_id,
        user_id=current_user.id,
        content=comment_data.content
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get("/task/{task_id}", response_model=List[CommentResponse])
def get_task_comments(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    comments = db.query(Comment).filter(Comment.task_id == task_id).all()
    return comments

@router.put("/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only author can update comment")
    comment.content = comment_data.content
    db.commit()
    db.refresh(comment)
    return comment

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only author can delete comment")
    db.delete(comment)
    db.commit()
    return None