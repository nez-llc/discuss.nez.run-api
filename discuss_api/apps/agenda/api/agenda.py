from django.shortcuts import get_object_or_404
from ninja import Router

from discuss_api.apps.agenda.models import Agenda
from discuss_api.apps.agenda.schema import AgendaOut, UpdownOut, UpdownIn
from discuss_api.apps.member.auth import TokenAuth


api = Router()


@api.get('/', response=list[AgendaOut])
def agenda_list_by_tag(request, tag_name: str = None):
    query = Agenda.objects.all()

    if tag_name:
        query = query.filter(tags__name=tag_name)

    return query


@api.get('/{agenda_id}', response=AgendaOut)
def get_agenda(request, agenda_id: int):
    agenda = get_object_or_404(Agenda, id=agenda_id)
    return agenda


@api.post('/{agenda_id}/updown', response={201: UpdownOut}, auth=TokenAuth())
def edit_agenda_updown(request, agenda_id: int, updown: UpdownIn):
    agenda = get_object_or_404(Agenda, id=agenda_id)
    agenda.add_updown(request.auth, updown.updown)
    return agenda.updown
