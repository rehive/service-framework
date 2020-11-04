from django.urls import include, path, re_path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = (
    # Public
    re_path(r'^activate/$', views.ActivateView.as_view(), name='activate'),
    re_path(r'^deactivate/$', views.DeactivateView.as_view(), name='deactivate'),

    # Admin
    re_path(r'^admin/company/$', views.AdminCompanyView.as_view(), name='admin-company')
)

urlpatterns = format_suffix_patterns(urlpatterns)