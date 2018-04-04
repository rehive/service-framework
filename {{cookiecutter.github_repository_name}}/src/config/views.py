from django.http import HttpResponse


def index(request):
    return HttpResponse("Welcome to the {{cookiecutter.app_name}} server!")
