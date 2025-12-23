from enum import Enum


class Role(str, Enum):
  ROOT="root"
  ADMIN = "Admin"
  AUDITOR = "Auditor"
  MAINTAINER = "Maintainer"


authorized_users_db = {
    "osama": {
      "password": "osama123",
      "role": Role.ADMIN
    },
    "maather": {
      "password": "maather123",
      "role": Role.AUDITOR
    },
    "shihab": {
      "password": "shihab123",
      "role": Role.MAINTAINER
    }
}


