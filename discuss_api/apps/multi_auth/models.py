import secrets

from django.contrib.auth import get_user_model
from django.db import models as m


User = get_user_model()


def default_token():
    return secrets.token_hex(32)


class Token(m.Model):
    user = m.ForeignKey(User, on_delete=m.CASCADE)
    value = m.CharField(max_length=256, default=default_token)
    time_created = m.DateTimeField(auto_now_add=True)
    # TODO : time_expired

    def __str__(self):
        return 'Token for {} ({})'.format(self.user, self.value)


class OAuth(m.Model):
    provider = m.CharField(max_length=16)
    id_on_provider = m.CharField(max_length=64)
    user = m.ForeignKey(User, on_delete=m.CASCADE)
    time_created = m.DateTimeField(auto_now_add=True)
    time_updated = m.DateTimeField(auto_now=True)

    def issue_token(self):
        return Token.objects.create(user=self.user)

    def __str__(self):
        return 'OAuth for {} ({})'.format(self.user, self.provider)
