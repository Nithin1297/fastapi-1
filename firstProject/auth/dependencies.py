from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from config.database import users_collection

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username  # Return username or user object as needed
    except JWTError:
        raise credentials_exception

def get_current_active_user(token: str = Depends(oauth2_scheme)):
    username = get_current_user(token)
    user = users_collection.find_one({"username": username})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def require_role(required_role: str):
    def role_checker(user: dict = Depends(get_current_active_user)):
        if user['role'] != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"
            )
        return user
    return role_checker