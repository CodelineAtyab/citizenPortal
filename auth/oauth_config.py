import os
from dotenv import load_dotenv


# Read the environment variables from .env file located in this project
load_dotenv()

"""
OAuth 2.0 / OpenID Connect Configuration for Google
"""
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

# Google OAuth configuration
# Get your Client ID and Client Secret from Google Cloud Console:
# https://console.cloud.google.com/apis/credentials
OAUTH_CLIENT_ID = os.environ.get("GCP_OAUTH_CLIENT_ID")
OAUTH_CLIENT_SECRET = os.environ.get("GCP_OAUTH_CLIENT_SECRET")

# Google OAuth endpoints (standard)
OAUTH_AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
OAUTH_ACCESS_TOKEN_URL = "https://oauth2.googleapis.com/token"
OAUTH_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
OAUTH_REDIRECT_URI = "http://localhost:8000/auth"

# Session configuration
SESSION_SECRET_KEY = os.environ.get("APP_SESSION_SECRET_KEY")

# Initialize OAuth
oauth = OAuth()

oauth.register(
    name='google',
    client_id=OAUTH_CLIENT_ID,
    client_secret=OAUTH_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)


def get_oauth_client():
    """Returns the configured Google OAuth client"""
    return oauth.google
