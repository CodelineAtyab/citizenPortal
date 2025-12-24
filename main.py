from typing import List
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

from app_logger import getLogger
from data_store import postgresql_db_store
from dto import User
from auth.http_basic_auth import verify_credentials, allowed_roles
from auth.rbac import Role
from auth.oauth_config import oauth, get_oauth_client, SESSION_SECRET_KEY, OAUTH_REDIRECT_URI


module_logger = getLogger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    module_logger.info("Initializing Database...")
    try:
        postgresql_db_store.initialize_db_with_sample_data()
        module_logger.info("Database initialized successfully.")
    except Exception as e:
        module_logger.error(f"Database initialization failed: {e}")
    yield
    module_logger.info("Shutting down...")

app = FastAPI(lifespan=lifespan)

# Add session middleware for OAuth
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)


@app.get("/login")
async def login(request: Request):
    """
    Initiates the OAuth login flow.
    Redirects user to the OAuth provider's authorization page.
    """
    module_logger.info("Initiating OAuth login flow")
    client = get_oauth_client()
    redirect_uri = OAUTH_REDIRECT_URI
    return await client.authorize_redirect(request, redirect_uri)


@app.get("/auth")
async def auth(request: Request):
    """
    OAuth callback endpoint.
    Handles the authorization code and exchanges it for an access token.
    """
    module_logger.info("Processing OAuth callback")
    try:
        client = get_oauth_client()
        token = await client.authorize_access_token(request)
        
        # Get user info from the token
        user_info = token.get('userinfo')
        if not user_info:
            # If userinfo is not in token, fetch it separately
            user_info = await client.userinfo(token=token)
        
        # Store user info in session
        request.session['user'] = dict(user_info)
        request.session['token'] = token
        
        module_logger.info(f"User logged in successfully: {user_info.get('email', 'unknown')}")
        
        return JSONResponse(content={
            "msg": "Successfully authenticated",
            "user": dict(user_info)
        })
    except Exception as e:
        module_logger.error(f"OAuth authentication failed: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@app.get("/logout")
async def logout(request: Request):
    """
    Logs out the user by clearing the session.
    """
    module_logger.info("Logging out user")
    request.session.clear()
    return JSONResponse(content={"msg": "Successfully logged out"})


@app.get("/me")
async def get_current_user(request: Request):
    """
    Returns the currently logged-in user's information.
    Useful for checking authentication status.
    """
    user = request.session.get('user')
    token = request.session.get('token')
    
    if not user or not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    # Optional: Check token expiration if it has an 'expires_at' field
    if 'expires_at' in token:
        import time
        if token['expires_at'] < time.time():
            request.session.clear()
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    
    return JSONResponse(content=user)


@app.get(path="/users", response_model=List[User])
def get_all_users(db=Depends(postgresql_db_store.get_db), 
                  username: str = Depends(allowed_roles(roles=[Role.ADMIN, Role.AUDITOR]))):
    module_logger.info(f"Retrieving all Users. Action performed by {username}")
    return postgresql_db_store.get_all_users(conn=db)


@app.get(path="/users/{given_cno}", response_model=User)
def get_specific_user(given_cno: str, db=Depends(postgresql_db_store.get_db), 
                      username: str = Depends(allowed_roles(roles=[Role.ADMIN, Role.AUDITOR]))):
    module_logger.info(f"Filtering the User by civil id no: {given_cno}")
    user = postgresql_db_store.get_user_by_contact_no(given_cno, conn=db)
    if user:
        module_logger.info(f"Successfully filtered: {user}")
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@app.post(path="/users")
def register_new_user(incoming_user_obj: User, 
                      db=Depends(postgresql_db_store.get_db),
                      username: str = Depends(allowed_roles(roles=[Role.ADMIN]))):
    module_logger.info(f"Creating a new User: {incoming_user_obj}")
    if postgresql_db_store.create_user(incoming_user_obj, conn=db):
        return JSONResponse(content={"msg": "Successfully Registered!"}, status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)