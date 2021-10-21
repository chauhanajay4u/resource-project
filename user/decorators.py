"""Decorators."""
from rest_framework.response import Response
from functools import wraps
from user import models
from user.services.user_info_service import UserInfoService
from user.serializers import AuthenticationSerializer
from .utils import NotAcceptableError
from rest_framework import  status


def session_authorize(user_id_key='pk', *args, **kwargs):
    """Decorator to add to the views for session authorisation."""
    def deco(f):
        def abstract_user_id(request):
            if request.method == 'GET':
                user_id = request.query_params.get(user_id_key)[0]
            else:
                user_id = request.data.get(user_id_key)
            return user_id

        def abstract_session_token(request):
            session_token_header_key = 'HTTP_SESSION_TOKEN'
            return request.META.get(session_token_header_key)

        @wraps(f)
        def decorated_function(*args, **kwargs):
            request = args[1]
            if kwargs.get(user_id_key):
                user_id = kwargs[user_id_key]
                kwargs.pop(user_id_key)
            else:
                user_id = abstract_user_id(request)
            auth_data = {
                'user_id': int(user_id) if user_id else None,
                'session_token': abstract_session_token(request),
                'is_admin': False
            }
            auth_serializer = AuthenticationSerializer(
                data=auth_data)
            auth_data['authorized'] = auth_serializer.is_valid(
            ) and auth_serializer.verify_and_update_session()
            auth_data['is_admin'] = UserInfoService(
                user_id=user_id).is_admin()
            return f(auth_data=auth_data, *args, **kwargs)
        return decorated_function
    return deco

def format_error(message):
    return {
        "error": [
            message,
        ]
    }

class MetaDataResponse(Response):
    meta_data_dict = {
        "meta": "",
        "data": {}
    }

    def __init__(self, *args, **kwargs):
        if args:
            MetaDataResponse.meta_data_dict["data"] = args[0]
            if len(args) >= 2:
                MetaDataResponse.meta_data_dict["meta"] = args[1]
            modified_args = tuple([MetaDataResponse.meta_data_dict])
        super(MetaDataResponse, self).__init__(*modified_args, **kwargs)

def catch_exception():
    def deco(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                return f(*args, **kwargs)

            except NotAcceptableError as e:
                return MetaDataResponse(format_error(e.response),
                                        e.meta, status=e.status)

            except Exception as e:
                return MetaDataResponse(
                    format_error(str(e)), getattr(e, "meta", ""),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return decorated_function
    return deco

