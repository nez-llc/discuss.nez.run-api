from datetime import datetime

from ninja import Schema, Router
from discuss_api.apps.agenda.models import Agenda


api = Router()


class AgendaOut(Schema):
    id: int
    title: str
    summary: str
    desc: str
    created_time: datetime


@api.get('/', response=list[AgendaOut])
def agenda_list(request):
    agendas = Agenda.objects.all()
    return agendas


@api.get('/{agenda_id}', response=AgendaOut)
def get_agenda(request, agenda_id):
    agenda = Agenda.objects.get(id=agenda_id)
    return agenda
