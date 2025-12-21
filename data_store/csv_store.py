import os
import traceback
# from dto import User

# from app_logger import getLogger

# # Create logs directory if it doesn't exist
# os.makedirs("./data", exist_ok=True)

# FILEPATH = "./data/records.csv"
# if not os.path.exists(FILEPATH):
#   with open(FILEPATH, "a") as csv_file:  # Create a new file if it doesn't exist
#     csv_file.write("name, email, civil id no\n")
#   getLogger().info(f"New CSV file {FILEPATH} created with headers.")

# def store_user_in_csv(user: User):
#   with open(FILEPATH, "a") as csv_file:
#     csv_file.write(f"{user.name}, {user.email}, {user.contact_no}\n")
#   getLogger().info(f"Stored user {user.contact_no} to the file {FILEPATH}")