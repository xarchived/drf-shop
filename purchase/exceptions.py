from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class LimitExceededError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _('order limit exceeded')


class EmptyPriceError(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = _('price not found')
