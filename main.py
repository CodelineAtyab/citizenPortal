from contextlib import asynccontextmanager
import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app_logger import getLogger
from data_store import postgresql_db_store
from auth.oauth_config import SESSION_SECRET_KEY
from controllers.user_controllers import router as user_router
from controllers.auth_controller import auth_router
from controllers.static_controllers import static_router


module_logger = getLogger()

async def initialize_database_with_retry():
    """Background task to initialize database with retries."""
    max_retries = 10
    retry_delay = 2  # seconds
    
    for attempt in range(1, max_retries + 1):
        try:
            postgresql_db_store.initialize_db_with_sample_data()
            module_logger.info("Database initialized successfully.")
            return
        except Exception as e:
            module_logger.warning(f"Database initialization failed (attempt {attempt}/{max_retries}): {e}")
            if attempt < max_retries:
                wait_time = retry_delay * (2 ** (attempt - 1))  # Exponential backoff
                module_logger.info(f"Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
            else:
                module_logger.error("Database initialization failed after all retries.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    module_logger.info("Starting database initialization in background...")
    # Start background task without awaiting it
    task = asyncio.create_task(initialize_database_with_retry())
    
    yield
    
    # Cleanup: cancel the task if still running
    if not task.done():
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
    module_logger.info("Shutting down...")

app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add session middleware for OAuth
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)

# Include routers
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(static_router)

# Mount static files at /static
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)