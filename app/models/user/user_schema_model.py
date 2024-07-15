from ..common.base_entity_model import BaseEntityModel


class UserModel(BaseEntityModel):
    name: str | None = None
    email: str | None = None
    password: str
