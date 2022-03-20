from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from discuss_api.apps.agenda.api import api as agenda_api
from discuss_api.apps.statistic.api import api as statistics_api
from discuss_api.apps.member.api import api as member_api
from discuss_api.apps.status.api import api as status_api


api = NinjaAPI()
api.add_router('agendas', agenda_api)
api.add_router('statistics', statistics_api)
api.add_router('members', member_api)
api.add_router('status', status_api)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
