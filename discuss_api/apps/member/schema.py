from typing import Optional
from ninja import Schema
from discuss_api.apps.member.models import UserProfile


class UserIn(Schema):
    nickname: str
    picture_id: Optional[str]


class UserOut(Schema):
    id: int
    nickname: str
    picture: Optional[str]

    @staticmethod
    def resolve_nickname(obj):
        try:
            return obj.profile.nickname
        except UserProfile.DoesNotExist:
            return ''

    @staticmethod
    def resolve_picture(obj):
        if obj.profile.picture.file:
            return obj.profile.picture.file.url
        else:
            return None
