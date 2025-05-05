import uuid

from django.utils.translation import gettext_lazy as _
from django.utils.encoding import smart_str
from rest_framework import authentication, exceptions, status
from rehive import Rehive, APIException

from .models import Company, User


class AuthenticationAPIException(exceptions.APIException):
    """
    Modify the API exception to support optionally setting the following values:

    - status_code
    - message

    This is required for ambiguous errors from the Rehive API.
    """

    def __init__(self, detail=None, code=None, status_code=None, message=None):
        if status_code:
            self.status_code = status_code

        if message:
            self.message = message

        super().__init__(detail, code)


class HeaderAuthentication(authentication.BaseAuthentication):
    """
    Authentication utility class.
    """

    @staticmethod
    def get_auth_header(request, name="token"):
        try:
            auth = request.META['HTTP_AUTHORIZATION'].split()
        except KeyError:
            return None

        if not auth or smart_str(auth[0].lower()) != name:
            return None

        if not auth[1]:
            return None

        return auth[1]


class RehiveAuthentication(HeaderAuthentication):
    """
    Generic Rehive authentication. Only checks that the token in the
    authorization header belongs to a valid user.
    """

    def _raise_exception(self, exc):
        """
        Raise a custom exception for authentication/authorization.
        """

        try:
            status_code = exc.status_code
        except AttributeError:
            status_code = None

        # Handle 429 throttling errors.
        if status_code == status.HTTP_429_TOO_MANY_REQUESTS:
            try:
                wait = int(exc.result.headers['Retry-After'])
            except (AttributeError, TypeError, KeyError):
                wait = None
            raise exceptions.Throttled(wait=wait)

        # Handle other unexpected errors (raise a 500 error).
        elif (not status_code or status_code not in (
                    status.HTTP_400_BAD_REQUEST,
                    status.HTTP_403_FORBIDDEN,
                    status.HTTP_401_UNAUTHORIZED,
                )):
            raise exc

        # Otherwise try and get data from the exception (if it exists).
        try:
            data = exc.data['data']
        except (AttributeError, TypeError, KeyError):
            data = None

        # Otherwise try and get a message from the exception (if it exists).
        try:
            message = exc.data['message']
        except (AttributeError, TypeError, KeyError):
            message = None

        # Use either the data or the message exists.
        detail = data or message

        raise AuthenticationAPIException(
            detail=detail, status_code=status_code, message=message
        )

    def authenticate(self, request):
        token = self.get_auth_header(request)
        rehive = Rehive(token)

        if not token:
            raise exceptions.NotAuthenticated()

        try:
            platform_user = rehive.auth.get()
        except APIException as exc:
            self._raise_exception(exc)

        try:
            company = Company.objects.get(
                identifier=platform_user['company'],
                active=True
            )
        except Company.DoesNotExist:
            raise exceptions.ValidationError(
                {"non_field_errors": [_("Inactive company.")]}
            )

        user, created = User.objects.get_or_create(
            identifier=uuid.UUID(platform_user['id']),
            company=company
        )

        # Inject the platform user object into the auth user.
        user._platform_user = platform_user

        return user, token


class RehiveGroupAuthentication(RehiveAuthentication):
    # List of Rehive user groups that are allowed.
    # An empty list means all user groups are allowed.
    groups = []

    def authenticate(self, request):
        user, token = super().authenticate(request)

        # Get a list of groups the user belongs to.
        groups = [g['name'] for g in user._platform_user['groups']]
        # If a list of groups is defined make sure only those groups are
        # allowed.
        if (self.groups
                and len(set(self.groups).intersection(groups)) <= 0):
            raise exceptions.PermissionDenied()

        return user, token


class AdminAuthentication(RehiveGroupAuthentication):
    """
    Only admin level users can access endpoints under this level.
    """

    groups = ["admin", "service",]


class UserAuthentication(RehiveGroupAuthentication):
    """
    All rehive users can access endpoints under this level.
    """

    pass
