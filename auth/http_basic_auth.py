from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated
import secrets


security = HTTPBasic()

# Simple in-memory user database (for demonstration only)
fake_users_db = {
    "osama": "osama123",
    "maather": "maather123",
    "shihab": "shihab123"
}

def verify_credentials(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    """
    Verify username and password against our database. 
    Uses constant-time comparison to prevent timing attacks. 
    """
    # Check if user exists
    if credentials.username not in fake_users_db: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    # Get the stored password
    correct_password = fake_users_db[credentials.username]
    
    # Use secrets.compare_digest for secure comparison
    # if credentials.password == correct_password  (Prone to timing attack)
    is_password_correct = secrets.compare_digest(
        credentials.password.encode("utf8"),
        correct_password.encode("utf8")
    )
    
    if not is_password_correct:
        raise HTTPException(
            status_code=status. HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return credentials.username
