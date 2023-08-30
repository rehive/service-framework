from collections import OrderedDict
from logging import getLogger

from django.http import Http404
from django.utils.encoding import force_str
from rest_framework import status
from rest_framework import exceptions, status
from rest_framework.views import set_rollback
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from django_rehive_extras.exceptions import DjangoBaseException

from config import settings


logger = getLogger('django')


class APIError(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('A server error occurred.')
    default_error_slug = 'internal_error'

    def __init__(self, detail=None, error_slug=None):
        if detail is not None:
            self.detail = force_str(detail)
            self.error_slug = force_str(error_slug)
        else:
            self.detail = force_str(self.default_detail)
            self.error_slug = force_str(self.default_error_slug)

    def __str__(self):
        return self.detail


def custom_exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            # Use the manually set message if it exists.
            if hasattr(exc, "message"):
                message = exc.message or ''
            # Otherwise construct the message from the details.
            else:
                message = ''
                for key in exc.detail:
                    try:
                        if isinstance(exc.detail[key], str):
                            message += exc.detail[key] + ' '
                        else:
                            for error in exc.detail[key]:
                                # Exclude duplicates.
                                if error not in message:
                                    message += error + ' '
                    except TypeError:
                        if key == 'non_field_errors':
                            message = exc.detail[key][0]
                        else:
                            message = _('Invalid request.')

                # Remove trailing whitespace.
                if message.endswith(' '):
                    message = message[:-1]

            data = OrderedDict([
                ('status', 'error'), ('message', message), ('data', exc.detail)
            ])
        else:
            data = OrderedDict([('status', 'error'), ('message', exc.detail)])

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    elif isinstance(exc, Http404):
        msg = _('Not found.')
        data = {'status': 'error', 'message': msg}

        set_rollback()
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    elif isinstance(exc, PermissionDenied):
        msg = _('Permission denied.')
        data = {'status': 'error', 'message': msg}

        set_rollback()
        return Response(data, status=status.HTTP_403_FORBIDDEN)

    elif isinstance(exc, DjangoBaseException):
        data = {'status': 'error', 'message': exc.default_detail}

        set_rollback()
        return Response(data, status=exc.status_code)

    # If debug is false return a formatted error and raise an internal error.
    if not settings.DEBUG:
        logger.exception(exc)
        exc = DjangoBaseException()
        return Response(
            {'status': 'error', 'message': exc.default_detail},
            status=exc.status_code
        )

    # Note: Unhandled exceptions will raise a 500 error.
    return None
