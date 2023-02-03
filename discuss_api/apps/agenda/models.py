from enum import Enum

from django.contrib.auth import get_user_model
from django.db import models as m

from discuss_api.apps.tag.models import Tag

User = get_user_model()


class Updown(str, Enum):
    UP = 'up'
    DOWN = 'down'
    NONE = None


class VoteChoice(Enum):
    AGREE = 'agree'
    NOT_AGREE = 'not_agree'
    NOT_SURE = 'not_sure'


class CommentStatus(str, Enum):
    ACTIVE = 0
    DELETED_BY_USER = 1
    DELETED_BY_ADMIN = 2
    DELETED_BY_WITHDRAWAL = 3

    def __str__(self):
        return self.name


class Agenda(m.Model):
    writer = m.ForeignKey(User, on_delete=m.CASCADE)
    title = m.CharField(max_length=150)
    summary = m.TextField()
    desc = m.TextField()

    created_time = m.DateTimeField(auto_now_add=True)
    updated_time = m.DateTimeField(auto_now=True)

    tags = m.ManyToManyField(Tag, related_name='agendas')

    @property
    def vote_count(self):
        agree_count = self.vote_history.filter(value=VoteChoice.AGREE).count()
        not_agree_count = self.vote_history.filter(value=VoteChoice.NOT_AGREE).count()
        not_sure_count = self.vote_history.filter(value=VoteChoice.NOT_SURE).count()

        return {
            'agree': agree_count,
            'not_agree': not_agree_count,
            'not_sure': not_sure_count,
        }

    def make_vote(self, user, value: VoteChoice):
        ballot, created = Vote.objects.get_or_create(agenda=self, voter=user)
        ballot.value = value
        ballot.save()
        return ballot

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

    def add_comment(self, user, content):
        comment, created = Comment.objects.get_or_create(agenda=self, writer=user, content=content)
        comment.save()
        return comment

    @property
    def comment_count(self):
        return self.comments.filter(status=CommentStatus.ACTIVE).count()

    def check_updown(self, user):
        try:
            return UpdownHistory.objects.get(agenda=self, voter=user).updown
        except UpdownHistory.DoesNotExist:
            return Updown.NONE

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
    agenda = m.ForeignKey(Agenda, on_delete=m.CASCADE, related_name='comments')
    content = m.TextField(default='')

    created_time = m.DateTimeField(auto_now_add=True)
    updated_time = m.DateTimeField(auto_now=True)

    status = m.CharField(
        max_length=25,
        choices=[(status.name, status.value) for status in CommentStatus],
        default=CommentStatus.ACTIVE
    )

    @property
    def agreement(self):
        return self.agreement_history.filter(comment=self).count()

    def add_agreement(self, user):
        history, created = AgreementHistory.objects.get_or_create(comment=self, voter=user)
        history.save()

    def delete_agreement(self, user):
        AgreementHistory.objects.get(comment=self, voter=user).delete()

    def __str__(self):
        return self.content


class AgreementHistory(m.Model):
    voter = m.ForeignKey(User, on_delete=m.CASCADE)
    comment = m.ForeignKey(Comment, on_delete=m.CASCADE, related_name='agreement_history')
    value = m.CharField(
        max_length=20, default=VoteChoice.NOT_SURE,
        choices=[(vote.name, vote.value) for vote in VoteChoice]
    )

    created_time = m.DateTimeField(auto_now_add=True)


class Vote(m.Model):
    voter = m.ForeignKey(User, on_delete=m.CASCADE)
    agenda = m.ForeignKey(Agenda, on_delete=m.CASCADE, related_name='vote_history')
    value = m.CharField(
        max_length=20,
        choices=[(vote.name, vote.value) for vote in VoteChoice]
    )

    created_time = m.DateTimeField(auto_now_add=True)
    updated_time = m.DateTimeField(auto_now=True)
