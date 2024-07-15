from ..common.base_entity_model import BaseEntityModel
from uuid import UUID
from pydantic import BaseModel


class NotificationModel(BaseEntityModel):
    receiver_id: str
    message: str
    send: bool = False
    payload: dict = {}


class SendNotificationInput(BaseModel):
    receiver_id: str
    message: str
    payload: dict = {}
