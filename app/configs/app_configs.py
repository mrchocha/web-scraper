import os

from app.models.common.db_configs import DBTypeEnum
from app.models.notification.notification_type_enum import NotificationTypeEnum
from ..common.errors import NotFoundError
from functools import cached_property


class __AppConfigs:
    @cached_property
    def get_notification_type(self) -> NotificationTypeEnum:
        try:
            env_notification_type = os.environ.get("NOTIFICATION_TYPE")
            if env_notification_type is None:
                return NotificationTypeEnum.LOCAL

            return NotificationTypeEnum[env_notification_type.upper()]
        except:
            return NotificationTypeEnum.LOCAL

    @cached_property
    def get_global_access_token(self) -> str:
        env_global_access_token = os.environ.get("GLOBAL_ACCESS_TOKEN")
        if env_global_access_token is None:
            raise NotFoundError(message=f"GLOBAL_ACCESS_TOKEN not defined/found")

        return env_global_access_token

    @cached_property
    def get_db_type(self) -> DBTypeEnum:
        try:
            env_db_type = os.environ.get("DB_TYPE")
            if env_db_type is None:
                raise DBTypeEnum.LOCAL

            return DBTypeEnum[env_db_type.upper()]
        except:
            return DBTypeEnum.LOCAL


AppConfigsInstance = __AppConfigs()
