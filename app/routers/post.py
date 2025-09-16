from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException,APIRouter
from sqlmodel import Session, func, select
from .. import models,schemes,auth2
from .. database import get_session
from sqlalchemy.orm import selectinload

router = APIRouter(
    prefix="/posts",tags=['posts']
)
@router.get("/",response_model_by_alias=List[schemes.pydanticPost])
def get_posts(session: Session = Depends(get_session), limit: int = 10, skip: int = 0, search: Optional[str] = None):
    # Base query joining posts and votes counting votes per post
    query = (select(models.Posts,func.count(models.Votes.post_id).label("votes"))
        .join(models.Votes, models.Posts.id == models.Votes.post_id, isouter=True)
        .group_by(models.Posts.id)
    )

    # Add search filter if provided
    if search:
        query = query.filter(models.Posts.title.contains(search))
    
    # Limit and offset for pagination
    query = query.limit(limit).offset(skip)
    
    # Execute the final query
    result = session.exec(query).mappings().all()
    return result


    
@router.post("/", response_model=schemes.PostResponse)
def create_post(pypost:schemes.PostCreate, session: Session = Depends(get_session),current_user: int=Depends(auth2.get_current_user)):
    new_post = models.Posts(owner_id=current_user.id , **pypost.model_dump())
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    if not new_post:
        raise HTTPException(status_code=404,detail='couldnt add post')
    return new_post





@router.get("/{post_id}", response_model=schemes.PostResponse)
def read_hero(post_id: int, session: Session = Depends(get_session)):
    statement = (
        select(
            models.Posts,
            func.count(models.Votes.post_id).label("votes")
        )
        .join(models.Votes, models.Posts.id == models.Votes.post_id, isouter=True)
        .options(selectinload(models.Posts.owner))
        .where(models.Posts.id == post_id)
        .group_by(models.Posts.id)
    )
    result = session.exec(statement).one_or_none()
    if not result:
        raise HTTPException(status_code=404, detail=f'post with id: {post_id} not found')

    post, votes = result
    return {**post.model_dump(), "owner": post.owner, "votes": votes}

@router.delete("/{post_id}")
def delete_post(post_id: int,session: Session = Depends(get_session),current_user: int = Depends(auth2.get_current_user)):
    deleted_post = session.get(models.Posts, post_id)
    if not deleted_post:
        raise HTTPException(status_code=404, detail='Post not found')
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=403,detail="cannot perform unauthorized action")
    session.delete(deleted_post)
    session.commit()
    return deleted_post



@router.put("/{post_id}",response_model=schemes.PostResponse)
def update_post(post_id: int, pypost:schemes.PostUpdate, session: Session = Depends(get_session),current_user=Depends(auth2.get_current_user)):
    # Fetch the existing post
    updated_post = session.get(models.Posts, post_id)
    if not updated_post:
        raise HTTPException(status_code=404, detail="Couldnt update Post")
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=403,detail="cannot perform unauthorized action")
    # Update the fields
    updated_post.title = pypost.title
    updated_post.content = pypost.content
    updated_post.published = pypost.published

    # Commit the changes
    session.commit()
    session.refresh(updated_post)
    print(current_user)
    return updated_post


"""@router.get("/",response_model=List[schemes.PostResponse])
def getuserposts(session:Session=Depends(auth2.get_session),current_user: int = Depends(auth2.get_current_user)):
    current_user_posts = session.exec(
    select(models.Posts).where(models.Posts.user_id == current_user.id)).all()
    if not current_user_posts:
        raise HTTPException(status_code=404,detail="no posts found")
    return current_user_posts"""