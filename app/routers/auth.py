from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import utils, oauth2, schemas
from ..database import get_db


router = APIRouter(
    tags=['Authentication']
)

# TODO: We will need to rework the return statement as we don't want to publicly return the token info
@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: tuple = Depends(get_db)):
    """Validate user login credentials"""

    # DB Connection
    conn, cursor = db

    cursor.execute("""SELECT * FROM users WHERE email = %s""", (user_credentials.username,))
    user = cursor.fetchone()

    # Check if user is in database
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # Check if verification process return valid or invalid
    if not utils.verify_credentials(user_credentials.password, user['password']):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # Create a Token
    access_token = oauth2.create_access_token(data = {"user_id": user["id"]})
    return {"access_token": access_token, "token_type": "bearer"}