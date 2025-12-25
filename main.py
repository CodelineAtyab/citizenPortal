from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from starlette.middleware.sessions import SessionMiddleware

from app_logger import getLogger
from data_store import postgresql_db_store
from auth.oauth_config import SESSION_SECRET_KEY
from controllers.user_controllers import router as user_router
from controllers.auth_controller import auth_router


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

# Include routers
app.include_router(user_router)
app.include_router(auth_router)


@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Serves the index.html file on the root URL.
    """
    index_path = Path(__file__).parent / "ui" / "index.html"
    if index_path.exists():
        return HTMLResponse(content=index_path.read_text(), status_code=200)
    else:
        raise HTTPException(status_code=404, detail="index.html not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)