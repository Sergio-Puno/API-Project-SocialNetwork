from passlib.context import CryptContext

# Set hash setting
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create hashing function for import
def hash(password: str):
    return pwd_context.hash(password)

# Create verification function for user login
def verify_credentials(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)