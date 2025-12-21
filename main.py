from typing import List
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app_logger import getLogger
from data_store import postgresql_db_store
from dto import User


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


@app.get(path="/users", response_model=List[User])
def get_all_users(db=Depends(postgresql_db_store.get_db)):
    module_logger.info("Retrieving all Users")
    return postgresql_db_store.get_all_users(conn=db)


@app.get(path="/users/{given_cno}", response_model=User)
def get_specific_user(given_cno: str, db=Depends(postgresql_db_store.get_db)):
    module_logger.info(f"Filtering the User by civil id no: {given_cno}")
    user = postgresql_db_store.get_user_by_contact_no(given_cno, conn=db)
    if user:
        module_logger.info(f"Successfully filtered: {user}")
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@app.post(path="/users")
def register_new_user(incoming_user_obj: User, db=Depends(postgresql_db_store.get_db)):
    module_logger.info(f"Creating a new User: {incoming_user_obj}")
    if postgresql_db_store.create_user(incoming_user_obj, conn=db):
        return JSONResponse(content={"msg": "Successfully Registered!"}, status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)