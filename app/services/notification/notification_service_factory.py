from app.configs import app_configs
from app.models.notification.notification_type_enum import NotificationTypeEnum
from .notification_service_interface import INotificationService
from .local_notification_service import __LocalNotificationService
from app.common.errors import NotFoundError


def __NotificationServiceFactory() -> INotificationService:
    notification_type = app_configs.AppConfigsInstance.get_notification_type
    match notification_type:
        case NotificationTypeEnum.LOCAL:
            return __LocalNotificationService()
        case _:
            raise NotFoundError(
                "Notification service not found for notification type '{notification_type}'",
            )


NotificationServiceInstance = __NotificationServiceFactory()
