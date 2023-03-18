from datetime import datetime
from typing import List, Any

from ninja import Schema
from ninja.pagination import PaginationBase

from discuss_api.apps.agenda.models import Updown, VoteChoice, CommentStatus
from discuss_api.apps.member.schema import UserOut


class CustomPagination(PaginationBase):
    class Input(Schema):
        skip: int = 0
        per_page: int = 10

    class Output(Schema):
        items: List[Any]
        total: int
        per_page: int
        current_page: int

    def paginate_queryset(self, queryset, pagination: Input, **params):
        skip = pagination.skip
        per_page = pagination.per_page
        return {
            'items': queryset[skip: skip + per_page],
            'total': queryset.count(),
            'per_page': per_page,
            'current_page': (skip + per_page) / per_page,
        }


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
    status: CommentStatus
    deleted: bool
    content: str
    created_time: datetime
    updated_time: datetime
    agreement: int
    agenda_id: int
    agenda_title: str

    @staticmethod
    def resolve_agenda_id(obj):
        return obj.agenda.id

    @staticmethod
    def resolve_agenda_title(obj):
        return obj.agenda.title


class CommentAgreementOut(Schema):
    total_agreement: int


class DeleteCommentOut(Schema):
    deleted_comment_id: int


class VoteIn(Schema):
    ballot: VoteChoice


class VoteOutCnt(Schema):
    very_agree: int
    agree: int
    very_disagree: int
    disagree: int
    neutral: int


class VoteOut(Schema):
    value: VoteChoice
    agenda_id: int
    voter_id: int


class AgendaIn(Schema):
    title: str
    summary: str
    desc: str
    tags: list[TagIn] = []


class AgendaOut(Schema):
    id: int
    writer: UserOut
    title: str
    summary: str
    desc: str
    created_time: datetime
    updated_time: datetime
    tags: list[TagOut]


class AgendaMyOut(Schema):
    my_updown: Updown


