from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException,APIRouter
from sqlmodel import Session, select
from .. import models,schemes,auth2
from .. database import get_session




router = APIRouter(prefix="/vote",tags=['Vote'])
@router.post("/", status_code=201)
def vote(vote: schemes.Vote, session: Session = Depends(get_session), current_user: int = Depends(auth2.get_current_user)):
    post_not_found=session.exec(select(models.Posts).where(models.Posts.id == vote.post_id)).first()
    if not post_not_found:
        raise HTTPException(status_code=404,detail="post not found")

    found_vote = session.exec(
        select(models.Votes).where(
            models.Votes.post_id == vote.post_id,
            models.Votes.user_id == current_user.id
        )
    ).first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=409, detail="user has already voted on post")
        new_vote = models.Votes(post_id=vote.post_id, user_id=current_user.id)
        session.add(new_vote)
        session.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=404, detail="vote does not exist")
        session.delete(found_vote)
        session.commit()
        return {"message": "successfully deleted vote"}
