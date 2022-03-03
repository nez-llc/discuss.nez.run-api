from ninja import Schema

from discuss_api.apps.member.models import UserProfile


class UserOut(Schema):
    id: int
    nickname: str

    @staticmethod
    def resolve_nickname(obj):
        try:
            return obj.profile.nickname
        except UserProfile.DoesNotExist:
            return ''
