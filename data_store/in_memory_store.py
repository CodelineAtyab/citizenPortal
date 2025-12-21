from dto import User
from typing import List

from app_logger import getLogger

module_logger = getLogger()

temp_user_store: List[User] = [
    User(name='Mr.A', email='mra@gmail.com', contact_no="12345678"),
    User(name='Mr.B', email='mrb@gmail.com', contact_no="12345679"),
    User(name='Mr.C', email='mrc@gmail.com', contact_no="12345671")
]

module_logger.info("Created a temporary dict as DB with 4 users.")