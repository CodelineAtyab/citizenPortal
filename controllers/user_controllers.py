from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app_logger import getLogger
from data_store import postgresql_db_store
from dto import User
from auth.http_basic_auth import allowed_roles
from auth.rbac import Role


module_logger = getLogger()

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[User])
def get_all_users(db=Depends(postgresql_db_store.get_db)):
    module_logger.info(f"Retrieving all Users.")
    return postgresql_db_store.get_all_users(conn=db)


@router.get("/{given_cno}", response_model=User)
def get_specific_user(given_cno: str, db=Depends(postgresql_db_store.get_db), 
                      username: str = Depends(allowed_roles(roles=[Role.ADMIN, Role.AUDITOR]))):
    module_logger.info(f"Filtering the User by civil id no: {given_cno}")
    user = postgresql_db_store.get_user_by_contact_no(given_cno, conn=db)
    if user:
        module_logger.info(f"Successfully filtered: {user}")
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.post("/")
def register_new_user(incoming_user_obj: User, 
                      db=Depends(postgresql_db_store.get_db),
                      username: str = Depends(allowed_roles(roles=[Role.ADMIN]))):
    module_logger.info(f"Creating a new User: {incoming_user_obj}")
    if postgresql_db_store.create_user(incoming_user_obj, conn=db):
        return JSONResponse(content={"msg": "Successfully Registered!"}, status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
