from rest_framework import viewsets

from discuss_api.apps.agenda.models import Agenda
from discuss_api.apps.agenda.serializers import AgendaSerializer


class AgendasViewSet(viewsets.ModelViewSet):
    serializer_class = AgendaSerializer
    queryset = Agenda.objects.all()
