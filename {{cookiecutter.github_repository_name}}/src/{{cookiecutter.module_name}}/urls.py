from django.urls import include, path, re_path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = (
    # Public
    re_path(r'^activate/$', views.ActivateView.as_view(), name='activate'),
    re_path(r'^deactivate/$', views.DeactivateView.as_view(), name='deactivate'),
    re_path(r'^external_currencies/$', views.ExternalCurrencyView.as_view(), name='external-currencies'),

    # Admin
    re_path(r'^admin/company/$', views.AdminCompanyView.as_view(), name='admin-company'),
    re_path(r'^admin/currencies/$', views.AdminCurrenciesView.as_view(), name='admin-currencies'),
    re_path(r'^admin/currencies/(?P<code>([a-zA-Z0-9\_\-]+))/$', views.AdminCurrencyView.as_view(), name='admin-currency'),
    re_path(r'^admin/transactions/$', views.AdminTransactionsView.as_view(), name='admin-transactions'),
    re_path(r'^admin/transactions/(?P<identifier>([a-zA-Z0-9\_\-]+))/$', views.AdminTransactionsView.as_view(), name='admin-transaction'),

    # User
    re_path(r'^user/$', views.UserView.as_view(), name='user'),
    re_path(r'^user/currencies/$', views.UserCurrenciesView.as_view(), name='user-currencies'),
    re_path(r'^user/currencies/(?P<code>([a-zA-Z0-9\_\-]+))/$$', views.UserCurrencyView.as_view(), name='user-currency'),
    re_path(r'^user/transactions/$', views.UserTransactionsView.as_view(), name='user-transactions'),
    re_path(r'^user/transactions/(?P<identifier>([a-zA-Z0-9\_\-]+))/$', views.UserTransactionsView.as_view(), name='user-transaction'),
)

urlpatterns = format_suffix_patterns(urlpatterns)