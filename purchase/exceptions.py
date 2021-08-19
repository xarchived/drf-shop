from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _


class LimitExceededError(APIException):
    status_code = 403
    default_detail = _('order limit exceeded')


class EmptyPriceError(APIException):
    status_code = 422
    default_detail = _('price not found')
