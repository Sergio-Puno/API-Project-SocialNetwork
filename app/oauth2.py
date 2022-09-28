from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database
import configparser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Auth Config Parameters
# Random generated string: Run `openssl rand -hex 32` in terminal
parser = configparser.ConfigParser()
parser.read("app/conn.conf")
SECRET_KEY = parser.get("api_config", "SECRET_KEY")
ALGORITHM = parser.get("api_config", "ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(parser.get("api_config", "ACCESS_TOKEN_EXPIRE_MINUTES"))

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