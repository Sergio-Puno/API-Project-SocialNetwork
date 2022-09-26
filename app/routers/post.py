from fastapi import status, HTTPException, Depends, Response, APIRouter
from typing import List
from .. import schemas
from ..database import get_db

# Initialize router and set the path prefix
router = APIRouter(
    prefix="/posts",
    tags=["Users"]
)

#-----------  GET  -----------#
@router.get("/",response_model=List[schemas.Post])
def get_posts(db: tuple = Depends(get_db)):
    """RETRIEVE ALL POST LISTINGS"""

    # DB Connection
    conn, cursor = db

    cursor.execute("""SELECT * FROM posts;""")
    posts = cursor.fetchall()
    return posts

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: tuple = Depends(get_db)):
    """RETRIEVE POST DETAILS FOR SUPPLIED POST ID"""

    # DB Connection
    conn, cursor = db

    cursor.execute("""SELECT * FROM posts WHERE id = %s;""", (str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found.")

    return post

#-----------  POST  -----------#
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post:schemas.PostCreate, db: tuple = Depends(get_db)):
    """SUBMIT A NEW POST"""

    # DB Connection
    conn, cursor = db

    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;""",
                    (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()

    return new_post

#----------- UPDATE  -----------#
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: tuple = Depends(get_db)):
    """UPDATE AN EXISTING POST"""

    # DB Connection
    conn, cursor = db

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} does not exist.")

    return updated_post

#-----------  DELETE  -----------#
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: tuple = Depends(get_db)):
    """REMOVE AN EXISTING POST COMPLETELY"""

    # DB Connection
    conn, cursor = db

    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *;""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} does not exist.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
