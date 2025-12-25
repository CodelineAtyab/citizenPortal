from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app_logger import getLogger
from data_store import postgresql_db_store
from auth.oauth_config import SESSION_SECRET_KEY
from controllers.user_controllers import router as user_router
from controllers.auth_controller import auth_router
from controllers.static_controllers import static_router


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
app.include_router(static_router)

# Mount static files at /static
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)