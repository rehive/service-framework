from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

from . import views

import debug_toolbar

admin.autodiscover()

urlpatterns = (
    # Dashboard
    url(r'^dashboard/', include(admin.site.urls)),
    # Views
    url(r'^api/', include('conversion.urls', namespace='conversion')),
)

# Add debug URL routes
if settings.DEBUG:
    urlpatterns = (
        url(r'^$', views.index, name='index'),
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ) + urlpatterns
