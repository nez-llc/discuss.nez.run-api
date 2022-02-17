from django.contrib.auth import get_user_model
from django.db import models as m


User = get_user_model()


class Token(m.Model):
    user = m.ForeignKey(User, on_delete=m.CASCADE)
    value = m.CharField(max_length=256)
    time_created = m.DateTimeField(auto_now_add=True)
    # TODO : time_expired
