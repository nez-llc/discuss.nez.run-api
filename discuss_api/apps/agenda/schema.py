from datetime import datetime

from ninja import Schema

from discuss_api.apps.agenda.models import Updown


class UpdownIn(Schema):
    updown: Updown


class UpdownOut(Schema):
    total: int
    up: int
    down: int


class TagOut(Schema):
    id: int
    name: str


class CommentOut(Schema):
    id: int
    content: str
    created_time: datetime
    updated_time: datetime
    agreement: int


class AgendaOut(Schema):
    id: int
    title: str
    summary: str
    desc: str
    created_time: datetime
    updated_time: datetime
    tags: list[TagOut]
    updown: UpdownOut
