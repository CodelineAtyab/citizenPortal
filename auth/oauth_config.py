"""
OAuth 2.0 / OpenID Connect Configuration for Google
"""
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

# Google OAuth configuration
# Get your Client ID and Client Secret from Google Cloud Console:
# https://console.cloud.google.com/apis/credentials
OAUTH_CLIENT_ID = "470641049682-h7l2eo4g7usad65po2as1cpq57db5uiu.apps.googleusercontent.com"
OAUTH_CLIENT_SECRET = "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"

# Google OAuth endpoints (standard)
OAUTH_AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
OAUTH_ACCESS_TOKEN_URL = "https://oauth2.googleapis.com/token"
OAUTH_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
OAUTH_REDIRECT_URI = "http://localhost:8000/auth"

# Session configuration
SESSION_SECRET_KEY = "your-secret-key-change-this-in-production"

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
