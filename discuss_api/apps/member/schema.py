from typing import Optional
from ninja import Schema
from discuss_api.apps.member.models import UserProfile
from discuss_api.apps.agenda.models import Comment
from discuss_api.apps.agenda.models import Comment, AgreementHistory, CommentVote


class UserIn(Schema):
    nickname: str
    picture_id: Optional[str]


class UserOut(Schema):
    id: int
    nickname: str
    picture: Optional[str]
    picture_id: Optional[str]
    date_joined: str
    active_point: int

    @staticmethod
    def resolve_nickname(obj):
        try:
            return obj.profile.nickname
        except UserProfile.DoesNotExist:
            return ''

    @staticmethod
    def resolve_picture(obj):
        try:
            if obj.profile.picture:
                return obj.profile.picture.file.url
            else:
                return None
        except UserProfile.DoesNotExist:
            return ''

    @staticmethod
    def resolve_picture_id(obj):
        try:
            if obj.profile.picture:
                return obj.profile.picture.id
            else:
                return None
        except UserProfile.DoesNotExist:
            return ''

    @staticmethod
    def resolve_date_joined(obj):
        try:
            d = obj.date_joined
            return d.strftime("%Y-%m-%d %I:%m:%S")
        except UserProfile.DoesNotExist:
            return ''

    @staticmethod
    def resolve_active_point(obj):
        comment = Comment.objects.filter(writer=obj)
        agree_count = AgreementHistory.objects.filter(comment__in=comment, value=CommentVote.AGREE).count()
        disagree_count = AgreementHistory.objects.filter(comment__in=comment, value=CommentVote.DISAGREE).count()

        return agree_count-disagree_count
