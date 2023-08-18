from django.urls import include, path, re_path
from django.contrib import admin
from django.conf import settings
from rest_framework import permissions
from drf_spectacular.views import (
    SpectacularJSONAPIView, SpectacularSwaggerView, SpectacularRedocView
)

from {{cookiecutter.module_name}}.urls import urlpatterns


admin.autodiscover()

urlpatterns = [
    # Administration
    re_path(r'^admin/', admin.site.urls),

    # Documentation
    re_path(
        r'^schema.json$',
        SpectacularJSONAPIView.as_view(
            api_version='1',
            urlconf=urlpatterns,
            custom_settings={
                'TITLE': '{{cookiecutter.project_name}} API',
                'DESCRIPTION': """
The **{{cookiecutter.project_name}} API**.
                    """,
                'VERSION': '1',
            }
        ),
        name='schema'
    ),
    re_path(
        r'^swagger/?$',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
    re_path(
        r'^/?$',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc-ui'
    ),

    # Views
    re_path(
        r'^api/',
        include(
            (
                '{{cookiecutter.module_name}}.urls',
                '{{cookiecutter.module_name}}'
            ),
            namespace='{{cookiecutter.module_name}}'
        )
    ),
]
