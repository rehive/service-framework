from drf_spectacular.extensions import OpenApiAuthenticationExtension


# Extensions

class UserAuthenticationScheme(OpenApiAuthenticationExtension):
    """
    Authentication extension for the custom APIAuthenticationclass.
    """

    target_class = '{{cookiecutter.module_name}}.authentication.UserAuthentication'
    name = 'apiAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': "Token-based HTTP Authentication scheme.\n"
                           "Include an API token in the `Authorization` header"
                           " using the format: `Token <your-api-key>`."
        }


class AdminAuthenticationScheme(UserAuthenticationScheme):
    target_class = '{{cookiecutter.module_name}}.authentication.AdminAuthentication'
    