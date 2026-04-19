from fastapi import APIRouter, status, Depends, HTTPException, Response
from .. import schemas, models
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional
from sqlalchemy import or_

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    
    new_post = models.Post(**post.dict())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), limit: int=10, skip: int=0, term: Optional[str]=""):
    
    posts = db.query(models.Post).filter(or_(models.Post.title.contains(term), models.Post.content.contains(term), models.Post.category.contains(term))).limit(limit).offset(skip).all()
    
    return posts

@router.get("/{id}", response_model=schemas.Post)
def get_one_post(id: int, db: Session = Depends(get_db)):
    
    post =db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    
    return post