from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse, RedirectResponse

from app_logger import getLogger
from auth.oauth_config import get_oauth_client, OAUTH_REDIRECT_URI


module_logger = getLogger()

auth_router = APIRouter(prefix="/auth", tags=["authentication"])


@auth_router.get("/login")
async def login(request: Request):
    """
    Initiates the OAuth login flow.
    Redirects user to the OAuth provider's authorization page.
    """
    module_logger.info("Initiating OAuth login flow")
    
    # Clear session to avoid state conflicts
    request.session.clear()
    
    client = get_oauth_client()
    redirect_uri = OAUTH_REDIRECT_URI
    return await client.authorize_redirect(request, redirect_uri)


@auth_router.get("/")
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
        
        return RedirectResponse(url="/static")
    except Exception as e:
        module_logger.error(f"OAuth authentication failed: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@auth_router.get("/logout")
async def logout(request: Request):
    """
    Logs out the user by clearing the session.
    """
    module_logger.info("Logging out user")
    request.session.clear()
    return JSONResponse(content={"msg": "Successfully logged out"})


@auth_router.get("/me")
async def get_current_user(request: Request):
    """
    Returns the currently logged-in user's information.
    Useful for checking authentication status.
    """
    request.session['extra'] = [1, 2, 3, 4]

    user = request.session.get('user')
    token = request.session.get('token')
    extra = request.session.get('extra ')
    
    if not user or not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    # Optional: Check token expiration if it has an 'expires_at' field
    if 'expires_at' in token:
        import time
        if token['expires_at'] < time.time():
            request.session.clear()
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    
    return JSONResponse(content=user)
