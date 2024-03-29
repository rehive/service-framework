from collections import OrderedDict
from logging import getLogger

from rest_framework import status, filters, exceptions
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view, permission_classes
from drf_rehive_extras.generics import *
from drf_rehive_extras.serializers import ActionResponseSerializer

from {{cookiecutter.module_name}}.authentication import AdminAuthentication
from {{cookiecutter.module_name}}.serializers import (
    ActivateSerializer, DeactivateSerializer, AdminCompanySerializer
)


logger = getLogger('django')


"""
Activation Endpoints
"""

class ActivateView(ActionAPIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)
    serializer_class = ActivateSerializer
    serializer_classes = {
        "POST": (ActivateSerializer, ActionResponseSerializer,)
    }


class DeactivateView(ActionAPIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)
    serializer_class = DeactivateSerializer
    serializer_classes = {
        "POST": (DeactivateSerializer, ActionResponseSerializer,)
    }


"""
Admin Endpoints
"""

class AdminCompanyView(RetrieveUpdateAPIView):
    serializer_class = AdminCompanySerializer
    authentication_classes = (AdminAuthentication,)

    def get_object(self):
        return self.request.user.company
