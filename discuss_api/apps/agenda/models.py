from enum import Enum

from django.contrib.auth import get_user_model
from django.db import models as m

from discuss_api.apps.tag.models import Tag


User = get_user_model()


class Updown(str, Enum):
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

    tags = m.ManyToManyField(Tag, related_name='agendas')

    @property
    def updown(self):
        up_count = self.updown_history.filter(updown=Updown.UP).count()
        down_count = self.updown_history.filter(updown=Updown.DOWN).count()

        return {
            'total': up_count - down_count,
            'up': up_count,
            'down': down_count,
        }

    def add_updown(self, user, updown: Updown):
        history, created = UpdownHistory.objects.get_or_create(agenda=self, voter=user)
        history.updown = updown
        history.save()

    def __str__(self):
        return self.title


class UpdownHistory(m.Model):
    voter = m.ForeignKey(User, on_delete=m.CASCADE)
    agenda = m.ForeignKey(Agenda, on_delete=m.CASCADE, related_name='updown_history')
    updown = m.CharField(
        max_length=20,
        choices=[(ud.name, ud.value) for ud in Updown]
    )
    created_time = m.DateTimeField(auto_now_add=True)
    updated_time = m.DateTimeField(auto_now=True)


class Comment(m.Model):
    writer = m.ForeignKey(User, on_delete=m.CASCADE)
    agenda = m.ForeignKey(Agenda, on_delete=m.CASCADE)

    # created_time = m.DateTimeField(auto_now_add=True)
    # updated_time = m.DateTimeField(auto_now=True)

    #TODO: 코멘트 내용, 추천 수, 코멘트 상태(회원 삭제, 관리자 삭제, 회원탈퇴)
    # content = m.TextField()
    # agreement_count = m.PositiveIntegerField()


class Vote(m.Model):
    voter = m.ForeignKey(User, on_delete=m.DO_NOTHING)
    agenda = m.ForeignKey(Agenda, on_delete=m.DO_NOTHING)
    value = m.CharField(
        max_length=20,
        choices=[(vote.name, vote.value) for vote in VoteChoice]
    )
    #created_time = m.DateTimeField(auto_now_add=True)
