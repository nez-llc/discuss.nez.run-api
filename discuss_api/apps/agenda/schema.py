from datetime import datetime

from ninja import Schema


class UpdownOut(Schema):
    total: int
    up: int
    down: int


class TagOut(Schema):
    id: int
    name: str


class AgendaOut(Schema):
    id: int
    title: str
    summary: str
    desc: str
    created_time: datetime
    tags: list[TagOut]
    updown: UpdownOut
