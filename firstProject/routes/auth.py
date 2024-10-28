from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from models.user_model import User  # Import your User model
from auth.auth import ALGORITHM, SECRET_KEY, hash_password, verify_password, create_access_token  # Import auth utilities
from config.database import users_collection  # Import users collection

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register/")
async def register(user: User):
    user.password = hash_password(user.password)  # Hash the password before storing it
    user.role = "user"  # Assign default role   
    users_collection.insert_one(dict(user))
    return {"message": "User registered successfully"}

@router.post("/token/")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data)
    user = users_collection.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"} 

@router.get("/users/me/")
async def read_users_me(token: str = Depends(oauth2_scheme)):
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
    except JWTError:
        raise credentials_exception

    user = users_collection.find_one({"username": username})
    if user is None:
        raise credentials_exception
    return {"username": user["username"], "email": user["email"]}

@router.get("/favicon.ico")
async def favicon():
    return {"message": "No favicon available"}