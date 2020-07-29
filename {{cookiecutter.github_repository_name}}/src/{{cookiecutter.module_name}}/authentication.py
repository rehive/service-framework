import uuid

from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_text
from rest_framework import authentication, exceptions
from rehive import Rehive, APIException

from .models import Company, User


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

        if not auth or smart_text(auth[0].lower()) != name:
            return None

        if not auth[1]:
            return None

        return auth[1]


class RehiveAuthentication(authentication.BaseAuthentication):
    # List of Rehive user groups that are allowed.
    # An empty list means all user groups are allowed.
    groups = []

    @staticmethod
    def get_auth_header(request, name="token"):
        try:
            auth = request.META['HTTP_AUTHORIZATION'].split()
        except KeyError:
            return None

        if not auth or smart_text(auth[0].lower()) != name:
            return None

        if not auth[1]:
            return None

        return auth[1]

    def authenticate(self, request):
        token = self.get_auth_header(request)
        rehive = Rehive(token)

        if not token:
            raise exceptions.AuthenticationFailed(
                _("Authentication credentials were not provided.")
            )

        try:
            platform_user = rehive.auth.get()
            # Get a list of groups the user belongs to.
            groups = [g['name'] for g in platform_user['groups']]
            # If a list of groups is defined make sure only those groups are
            # allowed.
            if (self.groups
                    and len(set(self.groups).intersection(groups)) <= 0):
                raise exceptions.AuthenticationFailed(_('Invalid user'))
        except APIException as exc:
            if (hasattr(exc, 'data')):
                message = exc.data['message']
            else:
                message = _('Invalid user')

            raise exceptions.AuthenticationFailed(message)

        try:
            company = Company.objects.get(
                identifier=platform_user['company'],
                active=True
            )
        except Company.DoesNotExist:
            raise exceptions.AuthenticationFailed(_("Inactive company."))

        user, created = User.objects.get_or_create(
            identifier=uuid.UUID(platform_user['id']),
            company=company
        )

        # Inject the platform user object into the auth user.
        user._platform_user = platform_user

        return user, token


class AdminAuthentication(RehiveAuthentication):
    """
    Only admin level users can access endpoints under this level.
    """

    groups = ["admin", "service",]


class UserAuthentication(RehiveAuthentication):
    """
    All rehive users can access endpoints under this level.
    """

    pass
