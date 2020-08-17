import datetime
import logging
import os

import requests
from tenacity import wait_exponential, retry, retry_if_exception_type, stop_after_attempt

from exception import ExternalServerCalledFailure

logger = logging.getLogger('root')


class TaskNoticeEventService:

    def __init__(self, event):
        self.event = event

    @retry(wait=wait_exponential(multiplier=1, min=5, max=20),
           stop=stop_after_attempt(15),
           retry=retry_if_exception_type(ExternalServerCalledFailure))
    async def celery_task_failed_notice(self):

        from event2call_task_notice_app import sanic_app
        subject = self.event['subject']
        now = datetime.datetime.now()
        data = {
            "msgtype": "text",
            "text": {
                "content": f"{now}\n {subject},赶紧瞅瞅！",
                "mentioned_list": ["@all"]
            }}
        response = requests.post(sanic_app.config.WX_ROBOT_WEB_HOOK, json=data)
        if response.status_code != 200:
            raise ExternalServerCalledFailure(f'response status code:{response.status_code}')
        else:
            logger.info(f'celery_task_failed_notice request WX_ROBOT_WEB_HOOK api response data: {response.json()}')
