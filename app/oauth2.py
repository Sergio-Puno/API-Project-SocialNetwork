from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# SECRET_KEY
SECRET_KEY = "198df2b8ddbafa9446d763b1f382fc974723b14d68965b2fa5e9c7fc4ef1c242"

# Algorithm 
ALGORITHM = "HS256"

# Expiration time: testing purposes set to 60
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    """Generate JWT (JSON Web Token) to client on validated login"""

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    """Validate token from client"""

    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        # token_data is currently just the user's id
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: tuple = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"}) 

    # DB Connection
    conn, cursor = db

    # Verify the token provided 
    token = verify_access_token(token=token, credentials_exception=credentials_exception)

    # Retrieve user information using ID provided
    cursor.execute("""SELECT * FROM users WHERE id = %s""", (token.id,))
    user_info = cursor.fetchone()

    return user_info