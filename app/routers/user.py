from fastapi import status, HTTPException, Depends,APIRouter
from .. import utils, schemas
from ..database import get_db

# Initialize router and set the path prefix
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

#----------- GET USER -----------#
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: tuple = Depends(get_db)):
    """SEARCH FOR USER INFORMATION BASED ON ID PROIVDED"""

    # DB Connection
    conn, cursor = db

    cursor.execute("""SELECT * FROM users WHERE id = %s;""", (str(id),))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist.")

    return user

#----------- CREATE USER -----------#
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: tuple = Depends(get_db)):
    """CREATE NEW USER AND ADD TO DATABASE: USERS"""

    # DB Connection
    conn, cursor = db

    # Hash password information
    hash_pw = utils.hash(user.password)
    user.password = hash_pw

    cursor.execute("""INSERT INTO users (email, password) VALUES(%s, %s) RETURNING *;""", (user.email, user.password))
    created_user = cursor.fetchone()
    conn.commit()

    return created_user