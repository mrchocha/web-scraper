from abc import abstractmethod, ABC

from app.models.common import request_context
from app.models.notification.notification_schema_model import SendNotificationInput


class INotificationService(ABC):
    @abstractmethod
    async def send(
        self,
        context: request_context.RequestContext,
        input: SendNotificationInput,
    ):
        pass
