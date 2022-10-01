from fastapi import status, HTTPException, Depends, Response, APIRouter
from typing import Optional, List
from .. import schemas, oauth2, models
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import func

# Initialize router and set the path prefix
router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# -----------  GET  ----------- #
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              limit: int = 10, search: Optional[str] = "", skip: int = 0):
    """RETRIEVE ALL POSTS BASED ON PARAMETERS"""

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
        .group_by(models.Post.id) \
        .filter(models.Post.title.contains(search)) \
        .limit(limit) \
        .offset(skip) \
        .all()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No posts found.")
    
    print()

    return posts


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """RETRIEVE POST DETAILS FOR SUPPLIED POST ID"""

    # Execute query
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
        .group_by(models.Post.id) \
        .filter(models.Post.id == id) \
        .first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found.")

    return post


# -----------  POST  ----------- #
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostCreate)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    """SUBMIT A NEW POST"""

    new_post = models.Post(owner=current_user.id, **post.dict())
    db.add(new_post)

    # Commit query to database
    db.commit()
    db.refresh()

    # test print for now to ensure we authenticate user and return the id parsed out from the request
    print(f"Current user: {current_user['email']}")

    return new_post


# ----------- UPDATE  ----------- #
@router.put("/{id}", response_model=schemas.PostCreate)
def update_post(id: int, revised_post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    """UPDATE AN EXISTING POST"""

    # Execute query
    update_query = db.query(models.Post).filter(models.Post.id == id)
    query_result = update_query.first()

    # Check if a value is returned from query
    if query_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} does not exist.")

    # Check if post user is == current logged-in user
    if query_result.id != current_user['id']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")

    # If there is a valid record and the user is the post owner, then commit the query
    update_query.update(revised_post.dict(), synchronize_session=False)
    db.commit()

    return query_result


# -----------  DELETE  ----------- #
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """REMOVE AN EXISTING POST COMPLETELY"""

    # Execute query
    delete_query = db.query(models.Post).filter(models.Post.id == id)
    query_result = delete_query.first()
    
    # Check if a value is returned from query
    if query_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} does not exist.")

    # Check if post user is == current logged-in user
    if query_result.id != current_user['id']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
    
    # If there is a valid record and the user is the post owner, then commit the query
    delete_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
