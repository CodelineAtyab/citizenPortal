from typing import List

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app_logger import getLogger
from data_store import in_memory_store, csv_store
from dto import User


module_logger = getLogger()

app = FastAPI()



@app.get(path="/users", response_model=List[User])
def get_all_users():
    module_logger.info("Retrieving all Users")
    return in_memory_store.temp_user_store


@app.get(path="/users/{given_cno}", response_model=User)
def get_specific_user(given_cno):
    module_logger.info(f"Filtering the User by civil id no: {given_cno}")
    result = next(filter(lambda curr_user: curr_user.contact_no == given_cno, in_memory_store.temp_user_store), User(name="Anonymous", email="unkown@unknown.com", contact_no="00000000"))
    module_logger.info(f"Successfully filtered: {result}")
    return result


@app.post(path="/users")
def register_new_user(incoming_user_obj: User):
    in_memory_store.temp_user_store.append(incoming_user_obj)
    csv_store.store_user_in_csv(incoming_user_obj)
    module_logger.info(f"Created a new User: {incoming_user_obj}")
    module_logger.debug(f"TESTING DEBUG LOG")
    return JSONResponse(content={"msg": "Successfully Registered!"}, status_code=201)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)