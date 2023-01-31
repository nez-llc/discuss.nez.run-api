from typing import Optional, List, Any
from ninja import Schema
from discuss_api.apps.member.models import UserProfile
from discuss_api.apps.agenda.models import Comment


class UserIn(Schema):
    nickname: str
    picture_id: Optional[str]


class UserOut(Schema):
    id: int
    nickname: str
    picture: Optional[str]
    picture_id: Optional[str]
    date_joined: str

    class Config():
        def __init__(self):
            pass

        arbitrary_types_allowed = True

    @staticmethod
    def resolve_comment(obj):
        print(obj.id)
        return Comment.objects.all().filter(writer=obj.id)

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
