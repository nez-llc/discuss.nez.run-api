from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from discuss_api.apps.agenda.api import api as agenda_api
from discuss_api.apps.statistic.api import api as statistics_api
from discuss_api.apps.status.api import api as status_api
from discuss_api.apps.member.api import api as member_api
from discuss_api.apps.multi_auth.api import api as auth_api
from discuss_api.apps.tag.api import api as tag_api


api = NinjaAPI()
api.add_router('agendas', agenda_api)
api.add_router('statistics', statistics_api)
api.add_router('status', status_api)
api.add_router('members', member_api)
api.add_router('auth', auth_api)
api.add_router('tags', tag_api)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]

urlpatterns += static('profile-pictures/', document_root='profile-pictures/')
