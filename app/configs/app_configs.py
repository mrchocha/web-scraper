import os

from app.models.common.db_configs import DBTypeEnum
from app.models.notification.notification_type_enum import NotificationTypeEnum
from ..common.errors import NotFoundError
from functools import cached_property


class __AppConfigs:
    ___GLOBAL_ACCESS_TOKEN = "bWc4eDJ6am1kamwzeTc2ZjdvZWt5bDRuMHVpNmp2Yjlicnc0czBpZm9pOXlzemxrc3pldm43Mmt2Ym12bnFyZnpxeThkdm82d3E5bWZkZWNzMG85YjMzZ3k4enRxYW16eWQyNzk3bmlhN3YwMTcxNnBzM29tOXM4bWdzbjd5cjY="

    @cached_property
    def get_notification_type(self) -> NotificationTypeEnum:
        return NotificationTypeEnum.LOCAL

    @cached_property
    def get_global_access_token(self) -> str:
        return self.___GLOBAL_ACCESS_TOKEN

    @cached_property
    def get_db_type(self) -> DBTypeEnum:
        return DBTypeEnum.LOCAL


AppConfigsInstance = __AppConfigs()
