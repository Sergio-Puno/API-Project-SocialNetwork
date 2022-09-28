from fastapi import status, HTTPException, Depends, Response, APIRouter
from .. import schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: tuple = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # DB Connection
    conn, cursor = db

    # Check if post user is trying to vote on exists
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(vote.post_id),))
    found_post = cursor.fetchone()
    
    if not found_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist.")

    # Query post + user composite key 
    cursor.execute("""SELECT * FROM votes WHERE post_id = %s AND user_id = %s;""", (str(vote.post_id), str(current_user["id"])))
    found_vote = cursor.fetchone()

    # User tries to like a post
    if vote.dir == 1:
        # Check if a vote is already in place for this use + post composite key, raise exception if true
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user['id']} has already votes on post id {vote.post_id}")

        # If a vote has not yet been submitted for this post / user
        cursor.execute("""INSERT INTO votes (post_id, user_id) VALUES (%s, %s)""", (vote.post_id, current_user['id']))
        conn.commit()
        
        return {"message": f"succesfully added vote to post {vote.post_id}"}
    
    # User tries to remove a like from a post
    else:
        # Cannot remove a like that doesnt not exist
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        
        cursor.execute("""DELETE FROM votes WHERE post_id = %s AND user_id = %s""", (vote.post_id, current_user["id"]))
        conn.commit()

        return {"message": f"successfully deleted vote from post {vote.post_id}"}
