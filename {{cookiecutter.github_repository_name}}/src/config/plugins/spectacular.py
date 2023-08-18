import os


SPECTACULAR_SETTINGS = {
    'TITLE': '{{cookiecutter.project_name}} API',
    'DESCRIPTION': '{{cookiecutter.project_name}} API',
    'TOS': 'https://rehive.com/terms/',
    'CONTACT': {
        "name": "",
        "url": "",
        "email": ""
    },
    'VERSION': '1',
    'EXTERNAL_DOCS': {
        "url": "",
        "description": ""
    },

    # List of servers.
    'SERVERS': [
        {"url": os.environ.get('BASE_URL', "")}
    ],

    # Swagger UI
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'SWAGGER_UI_SETTINGS': {
	    'docExpansion': 'none',
	    'showExtensions': False,
	    'defaultModelRendering': "example",
	    'displayOperationId': True
    },

    # Redoc
    'REDOC_DIST': 'SIDECAR',
    'REDOC_UI_SETTINGS': {
	    'lazyRendering': True,
	    'nativeScrollbars': True,
	    'requiredPropsFirst': True,
	    'showExtensions': True
    },

    # Disable `drf_spectacular.hooks.postprocess_schema_enums` to prevent
    # converting enums into components.
    'POSTPROCESSING_HOOKS': [],

    # Extensions
    'EXTENSIONS_INFO': {
        "x-logo": {
            "url": "",
            "href": "",
            "altText": ""
        }
    },
}
