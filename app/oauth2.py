from jose import JWTError, jwt
from datetime import datetime, timedelta
from .config import settings
from fastapi.security import OAuth2PasswordBearer
from .database import get_db, SessionLocal
from . import schemas
from fastapi import Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from . import schemas, database, models

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expiration})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")        
        if id is None:
            return False
        token_data = schemas.TokenData(id=str(id))
    except JWTError:
         return False   
    return token_data


def get_current_user(token: str, db: Session = Depends(get_db)):
    token = verify_access_token(token)
    if token:
        with SessionLocal() as db:
            user = db.query(models.User).filter(models.User.id == int(token.id)).first()
            if user:
                return user
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"user with id: {id} not found")
    return False

def verify_cookie(request: Request):
    token = request.cookies.get("Authorization")
    if token:
        user = get_current_user(token)
        if user:
            return user.id
        else:
            return False
    else:
        return False