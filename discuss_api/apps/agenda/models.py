from enum import Enum

from django.contrib.auth import get_user_model
from django.db import models as m
from django.db.models import TextChoices

from discuss_api.apps.tag.models import Tag

User = get_user_model()


class Updown(str, Enum):
    UP = 'up'
    DOWN = 'down'
    NONE = None


class VoteChoice(TextChoices, Enum):
    AGREE = 'agree', '찬성'
    VERY_AGREE = 'strongly_agree', '매우 찬성'
    DISAGREE = 'disagree', '반대'
    VERY_DISAGREE = 'strongly_disagree', '매우 반대'
    NEUTRAL = 'neither', '중립'


class CommentVoteChoice(str, Enum):
    AGREE = 'agree'
    DISAGREE = 'disagree'


class CommentStatus(TextChoices, Enum):
    ACTIVE = 'normal', '정상'
    DELETED_BY_USER = 'deleted_by_user', '사용자가 삭제'
    DELETED_BY_ADMIN = 'deleted_by_admin', '관리자에 의해 삭제'
    DELETED_BY_WITHDRAWAL = 'deleted_by_withdrawal', '탈퇴한 사용자의 댓글'


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
        return self.vote_history.aggregate(
            strongly_agree=m.Count('value', filter=m.Q(value=VoteChoice.VERY_AGREE)),
            agree=m.Count('value', filter=m.Q(value=VoteChoice.AGREE)),
            neither=m.Count('value', filter=m.Q(value=VoteChoice.NEUTRAL)),
            disagree=m.Count('value', filter=m.Q(value=VoteChoice.DISAGREE)),
            strongly_disagree=m.Count('value', filter=m.Q(value=VoteChoice.VERY_DISAGREE)),
        )

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
        choices=CommentStatus.choices,
        default=CommentStatus.ACTIVE,
    )

    @property
    def agreement(self):
        return self.agreement_history.filter(comment=self).count()

    @property
    def deleted(self):
        return self.status != CommentStatus.ACTIVE

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
        max_length=20,
        choices=[(commentVote.name, commentVote.value) for commentVote in CommentVoteChoice]
    )
    created_time = m.DateTimeField(auto_now_add=True)


class Vote(m.Model):
    voter = m.ForeignKey(User, on_delete=m.CASCADE)
    agenda = m.ForeignKey(Agenda, on_delete=m.CASCADE, related_name='vote_history')
    value = m.CharField(max_length=25, choices=VoteChoice.choices)

    created_time = m.DateTimeField(auto_now_add=True)
    updated_time = m.DateTimeField(auto_now=True)
