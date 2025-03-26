from pydantic import BaseModel

# User Registration Model
class UserCreate(BaseModel):
    username: str
    password: str
    role: str  # "admin" or "user"

# User Login Model
class UserLogin(BaseModel):
    username: str
    password: str

# Cypher Query Request Model
class QueryRequest(BaseModel):
    query: str
    params: dict = {}
