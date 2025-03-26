import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from database import db
from auth import get_current_user, create_access_token, verify_password, hash_password
from models import UserCreate, UserLogin, QueryRequest

app = FastAPI()

# Register User
@app.post("/register")
def register_user(user: UserCreate):
    hashed_password = hash_password(user.password)
    query = """
    CREATE (u:User {username: $username, password: $password, role: $role})
    RETURN u.username, u.role
    """
    result = db.execute_query(query, {"username": user.username, "password": hashed_password, "role": user.role})

    if not result:
        raise HTTPException(status_code=400, detail="User registration failed")

    return {"message": "User registered successfully"}

# Login & Get JWT Token
@app.post("/login")
def login(user: UserLogin):
    query = "MATCH (u:User {username: $username}) RETURN u.password AS password, u.role AS role"
    result = db.execute_query(query, {"username": user.username})

    if not result or not verify_password(user.password, result[0]["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.username, "role": result[0]["role"]})
    return {"access_token": access_token, "token_type": "bearer"}

# Execute Cypher Query (Admin Only)
@app.post("/execute")
def execute_cypher(request: QueryRequest, user: dict = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    return db.execute_query(request.query, request.params)

# Run Server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)
