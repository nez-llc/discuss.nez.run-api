from ninja.security import HttpBearer

from discuss_api.apps.member.models import Token


class TokenAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            token = Token.objects.get(value=token)
            return token.user
        except Token.DoesNotExist:
            return None
