import datetime

import jwt
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication


class JWTAuth(BaseAuthentication):
    secret_key = 'Eminescu era in Illuminati'
    options = {
        'verify_signature': True,
        'verify_exp': True,
        'verify_nbf': False,
        'verify_iat': True,
        'verify_aud': False
    }

    @classmethod
    def decode_jwt(cls, token):
        return jwt.decode(
            token,
            cls.secret_key,
            options=cls.options
        )

    @classmethod
    def create_jwt(cls, user_uuid):
        return jwt.encode({
            'some': 'payload',
            'id': str(user_uuid),
            'role': 'USER',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3500)
        },
            cls.secret_key,
            algorithm='HS256'
        ).decode('utf-8')

    def authenticate(self, request):
        auth = request.headers.get('Authorization')
        if auth:
            parts = auth.split()

            if parts[0].lower() != 'bearer':
                msg = _( "invalid header authorization")
                raise exceptions.AuthenticationFailed(msg)

            elif len(parts) == 1:
                msg = _("invalid header authorization")
                raise exceptions.AuthenticationFailed(msg)
            elif len(parts) > 2:
                msg = _("invalid header authorization")
                raise exceptions.AuthenticationFailed(msg)

            token = parts[1]
            try:
                user_data = JWTAuth.decode_jwt(token)

            except Exception as e:
                msg = _("invalid header authorization")
                raise exceptions.AuthenticationFailed(msg)
        else:
            msg = _("Missing Authorization")
            raise exceptions.AuthenticationFailed(msg)

        return user_data['id'], True
