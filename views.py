# pylint:disable=unused-argument
import logging

from sanic.response import json
from sanic.views import HTTPMethodView

from services import TaskNoticeEventService
import re
logger = logging.getLogger('root')


class EventView(HTTPMethodView):
    async def post(self, request, *args, **kwargs):
        try:

            delivery = request.headers['X-HfaxFK-Delivery']
            code_version = request.headers['User-Agent']
            data = request.json
            subject = data.get('subject')
            if re.match(r'.*(Celery){1}.*(Failed){1}.*', str(subject)):
                logger.info(
                    f'receive email celery task event: {delivery}, code version: {code_version}')
                await TaskNoticeEventService(data).celery_task_failed_notice()
        except Exception as e:
            logger.error(f'handle post data error:{e}')
        return json({'action': 'pong'})


class MockEventView(HTTPMethodView):
    async def post(self, request, *args, **kwargs):
        return json({'action': 'pong'})
