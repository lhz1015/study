import logging

from rest_framework import status
from redis.exceptions import RedisError
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler
from django.db import DatabaseError

logger = logging.getLogger('emp')


def exception_handler(exc, context):
    """
    自定义异常捕获
    :param exc:异常对象
    :param context: 抛出异常上下文(request,view)
    :return:
    """
    response = drf_exception_handler(exc, context)
    if not response:
        view = context.get('view')
        if isinstance(exc, DatabaseError):
            logger.error(f'[{view}] {exc}')
            response = Response({'message': "Mysql数据库异常"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
        elif isinstance(exc, RedisError):
            logger.error(f'[{view}] {exc}')
            response = Response({'message': "Redis数据库异常"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
    return response
