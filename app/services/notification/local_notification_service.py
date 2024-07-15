from app.models.common import request_context
from app.models.notification.notification_schema_model import SendNotificationInput
from .notification_service_interface import INotificationService


class __LocalNotificationService(INotificationService):
    async def send(
        self,
        context: request_context.RequestContext,
        input: SendNotificationInput,
    ):
        print(
            f"LocalNotificationService.send: sending notification to {input.receiver_id}"
        )
        print(
            f"NOTIFICATION!! To:{input.receiver_id}. {input.message}, payload: {input.payload}"
        )
