from django.urls import include, path, re_path
from django.contrib import admin
from django.conf import settings

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework import permissions

from . import views

import debug_toolbar

admin.autodiscover()

schema_view = get_schema_view(
   openapi.Info(
      title="{{cookiecutter.project_name}}} API",
      default_version='v1',
      description="Start by clicking Authorize and adding the header: "
       "Token <your-api-key>. The user endpoints require a normal "
       "rehive user token returned by Rehive's /auth/login/ or "
       "/auth/register/ endpoints."
   ),
   #validators=['flex', 'ssv'],
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=None),
        name='schema-json'),
    re_path(r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=None),
        name='schema-swagger-ui'),
    re_path(r'^$',
        schema_view.with_ui('redoc', cache_timeout=None),
        name='schema-redoc'),

    # Views
    re_path(r'^api/', include(('{{cookiecutter.module_name}}.urls','{{cookiecutter.module_name}'), namespace='{{cookiecutter.module_name}}')),
    re_path(r'^admin/', admin.site.urls),
]

# Add debug URL routes
if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
