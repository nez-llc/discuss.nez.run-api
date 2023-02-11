from datetime import datetime
from typing import List, Any

from ninja import Schema
from ninja.pagination import PaginationBase

from discuss_api.apps.agenda.models import Updown, VoteChoice, CommentStatus, CommentVote
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


class CommentVoteIn(Schema):
    ballot: CommentVote


class CommentVoteOut(Schema):
    agree: int
    disagree: int


class CommentOut(Schema):
    id: int
    writer: UserOut
    status: CommentStatus
    content: str
    created_time: datetime
    updated_time: datetime
    agreement: CommentVoteOut
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


class VoteOut(Schema):
    agree: int
    not_agree: int
    not_sure: int


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
    updown: UpdownOut
    vote_count: VoteOut
    comment_count: int


class AgendaMyOut(Schema):
    my_updown: Updown