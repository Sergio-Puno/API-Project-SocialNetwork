from fastapi import status, HTTPException, Depends, Response, APIRouter
from .. import schemas, oauth2, models
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # Check if the post exists
    found_post = db.query(models.Post) \
                .filter(models.Post.id == vote.post_id) \
                .first()
    
    if not found_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist.")

    # Query post + user composite key 
    vote_query = db.query(models.Vote) \
                .filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    
    found_vote = vote_query.first()

    # User tries to like a post
    if vote.dir == 1:
        # Check if a vote is already in place for this use + post composite key, raise exception if true
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                        detail=f"User {current_user.id} has already votes on post id {vote.post_id}")

        # If a vote has not yet been submitted for this post / user
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        
        return {"message": f"succesfully added vote to post {vote.post_id}"}
    
    # User tries to remove a like from a post
    else:
        # Cannot remove a like that doesnt not exist
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": f"successfully deleted vote from post {vote.post_id}"}
