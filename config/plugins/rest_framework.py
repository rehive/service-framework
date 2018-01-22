from rest_framework.settings import reload_api_settings

ANONYMOUS_USER_ID = -1

CORS_ORIGIN_ALLOW_ALL = True

# REST FRAMEWORK ~ http://www.django-rest-framework.org/
# ---------------------------------------------------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'conversion.permissions.IsAuthenticated',
    ),
    'EXCEPTION_HANDLER': 'config.exceptions.custom_exception_handler',
}

reload_api_settings(setting='REST_FRAMEWORK', value=REST_FRAMEWORK)
