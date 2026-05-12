"""
Custom Uvicorn worker for Gunicorn that disables ASGI lifespan protocol.
Django doesn't support the lifespan protocol, so we disable it to prevent errors.
"""
from uvicorn.workers import UvicornWorker as BaseUvicornWorker


class UvicornWorker(BaseUvicornWorker):
    """
    Uvicorn worker with lifespan protocol disabled.
    Use this with Gunicorn when running Django with ASGI.
    """

    CONFIG_KWARGS = {"lifespan": "off"}
