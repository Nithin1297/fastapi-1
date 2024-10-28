from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    password: str  # Store hashed password, not plain text
    role: str  # New field for user role