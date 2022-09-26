from jose import JWTError, jwt
from datetime import datetime, timedelta

# SECRET_KEY
SECRET_KEY = "198df2b8ddbafa9446d763b1f382fc974723b14d68965b2fa5e9c7fc4ef1c242"

# Algorithm 
ALGORITHM = "HS256"

# Expiration time
ACCESS_TOKEN_EXPIRE_MINUTES = 30   

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt