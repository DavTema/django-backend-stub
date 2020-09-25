import time
import logging

from api.aggregates import REQUEST_ID, LOCAL_THREAD, REQUEST_START_TIME


class CustomRequestPropertiesFilter(logging.Filter):
    def filter(self, record):
        if hasattr(LOCAL_THREAD, REQUEST_ID):
            record.request_id = getattr(LOCAL_THREAD, REQUEST_ID)

        if hasattr(LOCAL_THREAD, REQUEST_START_TIME):
            record.request_duration = round(time.time() - getattr(LOCAL_THREAD, REQUEST_START_TIME), 3)

        return True
