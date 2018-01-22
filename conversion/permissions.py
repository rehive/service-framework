from rest_framework import permissions
from logging import getLogger

logger = getLogger('django')


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if hasattr(request.user, "identifier"):
            return True
