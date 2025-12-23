import secrets

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated, Dict

from auth.rbac import authorized_users_db


security = HTTPBasic()

def allowed_roles(roles: list):
    def is_role_allowed(user_info: Annotated[Dict[str, str], Depends(verify_credentials)]):
        if user_info["role"] not in roles:
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Not allowed to access this resource. Your role is {user_info["role"].value}'
        )

    return is_role_allowed


def verify_credentials(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    """
    Verify username and password against our database. 
    Uses constant-time comparison to prevent timing attacks. 
    """
    # Check if user exists
    if credentials.username not in authorized_users_db: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    # Get the stored password
    correct_password = authorized_users_db[credentials.username]["password"]
    
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
    
    return authorized_users_db[credentials.username]
