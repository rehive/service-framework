from collections import OrderedDict
from logging import getLogger

from rest_framework import status, filters, exceptions
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view, permission_classes
from drf_rehive_extras.generics import *

from {{cookiecutter.module_name}}.authentication import AdminAuthentication
from {{cookiecutter.module_name}}.serializers import (
    ActivateSerializer, DeactivateSerializer, AdminCompanySerializer,
    ExternalCurrencySerializer, AdminCurrencySerializer, CurrencySerializer
)
from {{cookiecutter.module_name}}.models import (
    Company, User, Transaction, ExternalCurrency,
    Currency
)


logger = getLogger('django')


"""
Activation Endpoints
"""


class ActivateView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ActivateSerializer


class DeactivateView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = DeactivateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.delete()
        return Response({'status': 'success'})


"""
Public endpoints
"""
class ExternalCurrenciesView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ExternalCurrencySerializer

    def get_queryset(self):
        return ExternalCurrency.objects.all()


"""
Admin Endpoints
"""


class AdminCompanyView(RetrieveUpdateAPIView):
    serializer_class = AdminCompanySerializer
    authentication_classes = (AdminAuthentication,)

    def get_object(self):
        return self.request.user.company


class AdminCurrenciesView(ListAPIView):
    authentication_classes = (AdminAuthentication,)
    serializer_class = AdminCurrencySerializer

    def get_queryset(self):
        return Currency.objects.filter(
            company=self.request.user.company
        )


class AdminCurrencyView(RetrieveUpdateAPIView):
    authentication_classes = (AdminAuthentication,)
    serializer_class = AdminCurrencySerializer

    def get_object(self):
        try:
            return Currency.objects.get(
                company=self.request.user.company,
                code=self.kwargs.get('code')
            )
        except Currency.DoesNotExist:
            raise exceptions.NotFound()


class AdminTransactionsView(ListAPIView):
    authentication_classes = (AdminAuthentication,)
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transactions.objects.filter(
            company=self.request.user.company
        )


class AdminTransactionsView(RetrieveAPIView):
    authentication_classes = (AdminAuthentication,)
    serializer_class = TransactionSerializer

    def get_object(self):
        return Transactions.objects.get(
            company=self.request.user.company,
            identifier=self.kwargs.get('identifier')
        )


"""
User Endpoints
"""


class UserView(RetrieveAPIView):
    authentication_classes = (UserAuthentication,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserCurrenciesView(ListAPIView):
    authentication_classes = (UserAuthentication,)
    serializer_class = CurrencySerializer

    def get_queryset(self):
        return Currency.objects.filter(
            company=self.request.user.company
        )


class UserCurrencyView(RetrieveAPIView):
    authentication_classes = (UserAuthentication,)
    serializer_class = CurrencySerializer

    def get_object(self):
        try:
            return Currency.objects.get(
                company=self.request.user.company,
                code=self.kwargs.get('code')
            )
        except Currency.DoesNotExist:
            raise exceptions.NotFound()


class UserTransactionsView(ListAPIView):
    authentication_classes = (UserAuthentication,)
    serializer_class = TransactionSerializer

    def get_queryset(self):
        # TODO: Include filters that link a user to a transactions
        return Transaction.objects.filter()


class UserTransactionView(RetrieveAPIView):
    authentication_classes = (UserAuthentication,)
    serializer_class = TransactionSerializer

    def get_object(self):
        # TODO: Include filters that link a user to a transactions
        return Transaction.objects.get()

