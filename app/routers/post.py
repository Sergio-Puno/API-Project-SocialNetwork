from operator import concat
from fastapi import status, HTTPException, Depends, Response, APIRouter
from typing import List, Optional
from .. import schemas, oauth2
from ..database import get_db

# Initialize router and set the path prefix
router = APIRouter(
    prefix="/posts",
    tags=["Users"]
)

#-----------  GET  -----------#
@router.get("/",response_model=List[schemas.Post])
def get_posts(db: tuple = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
            limit: int = 10, search: Optional[str] = ""):
    """RETRIEVE POSTS BASED ON PARAMETERS"""

    # DB Connection
    conn, cursor = db

    # Split search into individual words
    search_terms = search.split(' ')

    # Build query
    query = f"""SELECT * FROM posts WHERE title ILIKE '%' || '{search_terms[0]}' || '%'"""
    
    for term in search_terms[1:]:
        modular_query = f""" OR title ILIKE '%' || '{term}' || '%'"""
        query = concat(query, modular_query)

    #cursor.execute("""SELECT * FROM posts WHERE title ILIKE '%%' || %s || '%%' LIMIT %s;""", (search, limit))
    # Execute query
    cursor.execute(query)
    posts = cursor.fetchall()
    
    return posts

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: tuple = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """RETRIEVE POST DETAILS FOR SUPPLIED POST ID"""

    # DB Connection
    conn, cursor = db

    # Execute query
    cursor.execute("""SELECT * FROM posts WHERE id = %s;""", (str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found.")

    return post

#-----------  POST  -----------#
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post:schemas.PostCreate, db: tuple = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """SUBMIT A NEW POST"""

    # DB Connection
    conn, cursor = db

    # Execute query
    cursor.execute("""INSERT INTO posts (title, content, published, user_id) VALUES (%s, %s, %s, %s) RETURNING *;""",
                    (post.title, post.content, post.published, current_user['id']))
    new_post = cursor.fetchone()

    # Commit query to database
    conn.commit()

    # test print for now to ensure we authenticate user and return the id parsed out from the request
    print(f"Current user: {current_user['email']}")

    return new_post

#----------- UPDATE  -----------#
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: tuple = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """UPDATE AN EXISTING POST"""

    # DB Connection
    conn, cursor = db

    # Execute query
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()["id"]

    # Check if a value is returned from query
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} does not exist.")

    # Check if post user is == current logged in user
    if update_post != current_user['id']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")

    # If there is a valid record and the user is the post owner, then commit the query
    conn.commit()

    return updated_post

#-----------  DELETE  -----------#
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: tuple = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """REMOVE AN EXISTING POST COMPLETELY"""

    # DB Connection
    conn, cursor = db

    # Execute query
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *;""", (str(id),))
    deleted_post = cursor.fetchone()["id"]
    
    # Check if a value is returned from query
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} does not exist.")

    # Check if post user is == current logged in user
    if deleted_post != current_user['id']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
    
    # If there is a valid record and the user is the post owner, then commit the query
    conn.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
