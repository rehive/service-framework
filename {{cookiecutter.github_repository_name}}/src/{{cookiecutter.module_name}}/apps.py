from django.apps import AppConfig


class {{cookiecutter.module_name}}AppConfig(AppConfig):
    name = '{{cookiecutter.module_name}}'

    def ready(self):
        import config.schema
