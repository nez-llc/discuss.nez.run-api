from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError
from ninja.pagination import paginate

from discuss_api.apps.agenda.models import Agenda, User
from discuss_api.apps.agenda.schema import AgendaOut, UpdownOut, UpdownIn, VoteOut, VoteIn, AgendaIn, CustomPagination, \
    AgendaDetailOut
from discuss_api.apps.multi_auth.auth import TokenAuth
from discuss_api.apps.tag.models import Tag


api = Router()


@api.get('/', response=list[AgendaOut])
@paginate(CustomPagination)
def agenda_list_by_tag(request, tag_name: str = None):
    query = Agenda.objects.all()

    if tag_name:
        query = query.filter(tags__name=tag_name)

    return query


@api.get('/{agenda_id}', response=AgendaDetailOut,  auth=TokenAuth())
def get_agenda(request, agenda_id: int):
    agenda = get_object_or_404(Agenda, id=agenda_id)

    # auth = User(TokenAuth())
    if request.auth:
        agenda.check_updown(request.auth)

    return agenda


@api.post('/', response={201: AgendaOut}, auth=TokenAuth())
def insert_agenda(request, agenda_in: AgendaIn):
    agenda = Agenda.objects.create(
        writer=request.auth,
        title=agenda_in.title,
        summary=agenda_in.summary,
        desc=agenda_in.desc,
    )

    for tag_id in agenda_in.tags:
        tag = Tag.objects.get(tag_id)
        agenda.tags.add(tag)

    return agenda


@api.post('/{agenda_id}', response={201: AgendaOut}, auth=TokenAuth())
def edit_agenda(request, agenda_id: int, agenda_in: AgendaIn):
    agenda = get_object_or_404(Agenda, id=agenda_id)

    if not request.auth:
        raise HttpError(401, 'Unauthorized')

    if request.auth != agenda.writer:
        raise HttpError(403, 'You don\'t have permission to access')

    agenda.title = agenda_in.title
    agenda.summary = agenda_in.summary
    agenda.desc = agenda_in.desc

    for tag_id in agenda_in.tags:
        tag = Tag.objects.get(id=tag_id)
        agenda.tags.add(tag)

    agenda.save()

    return agenda


@api.post('/{agenda_id}/updown', response={201: UpdownOut}, auth=TokenAuth())
def edit_agenda_updown(request, agenda_id: int, updown: UpdownIn):
    agenda = get_object_or_404(Agenda, id=agenda_id)
    agenda.add_updown(request.auth, updown.updown)
    return agenda.updown


@api.post('/{agenda_id}/votes', response={201: VoteOut}, auth=TokenAuth())
def vote_on_the_agenda(request, agenda_id: int, vote: VoteIn):
    agenda = Agenda.objects.get(id=agenda_id)
    agenda.make_vote(user=request.auth, value=vote.ballot)
    return agenda.vote_count
