from rest_framework import serializers

from discuss_api.apps.agenda.models import Agenda


class AgendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agenda
        fields = ['id', 'title', 'summary', 'desc']
