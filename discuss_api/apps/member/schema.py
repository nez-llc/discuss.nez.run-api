from typing import Optional
from ninja import Schema


class UserIn(Schema):
    nickname: str
    picture_id: Optional[str]


class UserOut(Schema):
    id: int
    nickname: str
    picture: Optional[str]

    @staticmethod
    def resolve_nickname(obj):
        return obj.profile.nickname

    @staticmethod
    def resolve_picture(obj):
        if obj.profile.picture:
            return obj.profile.picture.file.url
        else:
            return None
