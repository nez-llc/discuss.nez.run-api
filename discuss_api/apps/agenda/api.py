from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.security import django_auth

from discuss_api.apps.agenda.models import Agenda, Updown
from discuss_api.apps.agenda.schema import AgendaOut, UpdownOut


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


@api.post('/{agenda_id}/updown', response=UpdownOut, auth=django_auth)
def edit_agenda_updown(request, agenda_id: int, updown: Updown):
    agenda = get_object_or_404(Agenda, id=agenda_id)
    agenda.add_updown(request.auth, updown)
    return agenda.updown
