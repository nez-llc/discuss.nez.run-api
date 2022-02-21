from django.contrib import admin
from discuss_api.apps.agenda.models import Agenda, Comment


admin.site.register(Agenda)
admin.site.register(Comment)
