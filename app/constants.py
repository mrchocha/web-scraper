from .models.user.user_schema_model import UserModel
from datetime import datetime
from uuid import UUID

GLOBAL_USER_ID = "3f50b493-e93b-4eb7-bd49-7a32c4652361"
GLOBAL_USER = UserModel(
    id=GLOBAL_USER_ID,
    name="rahul",
    email="rahulahir4530@gmail.com",
    created_at=datetime.now().isoformat(),
    updated_at=datetime.now().isoformat(),
    password="",
)
