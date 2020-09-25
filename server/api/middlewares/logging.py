import uuid
import logging
from time import time

from sentry_sdk import configure_scope

from api.aggregates import REQUEST_ID, LOCAL_THREAD, REQUEST_START_TIME

logger = logging.getLogger(__name__)


class CustomRequestPropertiesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        params = (
            (REQUEST_ID, self.request_id),
            (REQUEST_START_TIME, time.time())
        )

        for key, value in params:
            self._remove_param_from_thread_local(key)
            self._propagate_param_to_thread_local(key, value)

        return self.get_response(request)

    @property
    def request_id(self):
        return uuid.uuid4().hex

    @staticmethod
    def _propagate_param_to_thread_local(key, value):
        setattr(LOCAL_THREAD, key, value)
        with configure_scope() as scope:
            scope.set_extra(key, value)

    @staticmethod
    def _remove_param_from_thread_local(key):
        if hasattr(LOCAL_THREAD, key):
            delattr(LOCAL_THREAD, key)
            with configure_scope() as scope:
                scope.remove_extra(key)
