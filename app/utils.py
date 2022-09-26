from passlib.context import CryptContext

# Set hash setting
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create hashing function for import
def hash(password: str):
    return pwd_context.hash(password)