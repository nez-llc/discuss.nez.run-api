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
    picture_id: Optional[str]

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
                return obj.profile.picture.file
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
