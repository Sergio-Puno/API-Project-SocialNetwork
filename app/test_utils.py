from passlib.context import CryptContext

# Script to create some passwords for offline testing

# Set hash setting
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

pw = 'password123'
hashed_pw = pwd_context.hash(pw)
print(hashed_pw)
