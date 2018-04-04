from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = (
    # Public
    url(r'^$', views.root),
    url(r'^activate/$', views.ActivateView.as_view(), name='activate'),
    url(r'^deactivate/$', views.DeactivateView.as_view(), name='deactivate'),

    # Admin
    url(r'^admin/company/$', views.AdminCompanyView.as_view(), name='admin-company'),
    url(r'^admin/currencies/$', views.AdminCurrencyListView.as_view(), name='admin-currencies'),
    url(r'^admin/currencies/(?P<code>(\w+))/$', views.AdminCurrencyView.as_view(), name='admin-currencies-view'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
