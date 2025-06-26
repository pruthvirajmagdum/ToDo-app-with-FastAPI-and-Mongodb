import os
from dotenv import load_dotenv
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import cast

load_dotenv()

# Get secret key and algorithm, raise if missing
secret = os.getenv("JWT_SECRET")
algorithm = os.getenv("JWT_ALGORITHM")

if not secret or not algorithm:
    raise RuntimeError("JWT_SECRET or JWT_ALGORITHM not set in environment variables")

# Safe for Pylance
SECRET_KEY = cast(str, secret)
ALGORITHM = cast(str, algorithm)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
