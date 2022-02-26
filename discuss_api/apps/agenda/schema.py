from datetime import datetime

from ninja import Schema

from discuss_api.apps.agenda.models import Updown, VoteChoice
from discuss_api.apps.member.schema import UserOut


class UpdownIn(Schema):
    updown: Updown


class UpdownOut(Schema):
    total: int
    up: int
    down: int


class TagIn(Schema):
    id: int


class TagOut(Schema):
    id: int
    name: str


class CommentIn(Schema):
    content: str = ''


class CommentOut(Schema):
    id: int
    writer: UserOut
    content: str
    created_time: datetime
    updated_time: datetime
    agreement: int


class VoteIn(Schema):
    ballot: VoteChoice


class VoteOut(Schema):
    agree: int
    not_agree: int
    not_sure: int


class AgendaIn(Schema):
    title: str
    summary: str
    desc: str
    tags: list[TagIn] = ''


class AgendaOut(Schema):
    id: int
    writer: UserOut
    title: str
    summary: str
    desc: str
    created_time: datetime
    updated_time: datetime
    tags: list[TagOut]
    updown: UpdownOut
    vote: VoteOut
