from fastapi import status, HTTPException, Depends,APIRouter
from .. import utils, schemas, models
from ..database import get_db
from sqlalchemy.orm import Session

# Initialize router and set the path prefix
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

#----------- GET USER -----------#
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    """SEARCH FOR USER INFORMATION BASED ON ID PROIVDED"""

    user = db.query(models.User) \
            .filter(models.User.id == id) \
            .first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist.")

    return user

#----------- CREATE USER -----------#
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """CREATE NEW USER AND ADD TO DATABASE: USERS"""

    # Hash password information
    hash_pw = utils.hash(user.password)
    user.password = hash_pw

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user