import os


def _get_response_context(exc):
    """
    Extract response context from known exception types.
    """

    from requests.exceptions import HTTPError
    from rehive import APIException

    if isinstance(exc, HTTPError) and exc.response is not None:
        response = exc.response
        try:
            body = response.json()
        except Exception:
            body = response.text[:2000] if response.text else None

        return {
            "status_code": response.status_code,
            "body": body,
            "url": response.url,
        }

    if isinstance(exc, APIException):
        result = getattr(exc, "result", None)
        try:
            body = result.json()
        except Exception:
            body = result.text[:2000] if result.text else None

        return {
            "status_code": exc.status_code,
            "body": body,
            "url": result.url,
        }

    return None


def before_send(event, hint):
    """
    Enrich Sentry events with HTTP response context for exceptions.
    """

    if "exc_info" in hint:
        context = _get_response_context(hint["exc_info"][1])
        if context:
            event.setdefault("contexts", {})["response"] = context

    return event


if os.environ.get('SENTRY_DSN_KEY'):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    # Sentry SDK
    sentry_sdk.init(
        os.environ.get('SENTRY_DSN_KEY'),
        integrations=[DjangoIntegration()],
        environment=os.environ.get('SENTRY_ENV'),
        before_send=before_send,
    )
