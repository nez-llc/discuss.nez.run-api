from enum import Enum

from django.contrib.auth import get_user_model
from django.db import models as m


User = get_user_model()


class Updown(Enum):
    UP = 'up'
    DOWN = 'down'


class VoteChoice(Enum):
    AGREE = 'agree'
    NOT_AGREE = 'not_agree'
    NOT_SURE = 'not_sure'


class Agenda(m.Model):
    writer = m.ForeignKey(User, on_delete=m.CASCADE)

    title = m.CharField(max_length=150)
    summary = m.TextField()
    desc = m.TextField()

    created_time = m.DateTimeField(auto_now_add=True)
    updated_time = m.DateTimeField(auto_now=True)


class Comment(m.Model):
    writer = m.ForeignKey(User, on_delete=m.CASCADE)
    agenda = m.ForeignKey(Agenda, on_delete=m.CASCADE)


class Vote(m.Model):
    voter = m.ForeignKey(User, on_delete=m.DO_NOTHING)
    agenda = m.ForeignKey(Agenda, on_delete=m.DO_NOTHING)
    value = m.CharField(
        max_length=20,
        choices=[(vote.name, vote.value) for vote in VoteChoice]
    )
