from apps.account import queries as accountQueries
from django.http import HttpResponseNotFound
from django.conf import settings
import jwt
import logging
logger = logging.getLogger('django')


def error_log_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        if response.status_code not in [200, 201, 203] and 'api' in request.path.split('/'):
            if isinstance(response, HttpResponseNotFound):
                data = None
            else:
                try:
                    data = response.data
                except Exception:
                    data = None
            msg = {
                'user': request.user.username,
                'method': request.method,
                'resource': request.path,
                'response': data
            }
            logger.info(msg)

        return response

    return middleware


def inject_user_lang_middleware(get_response):  # It does not work
    def middleware(request):
        # To return the results in user's language
        if request.user and request.META.get('HTTP_AUTHORIZATION'):
            token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
            if token:
                try:
                    payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=["HS256"])
                    user = accountQueries.get_user_by_id(id=payload['user_id'])
                    request.META['HTTP_ACCEPT_LANGUAGE'] = user.lang
                except Exception:
                    pass
        response = get_response(request)
        return response
    return middleware
