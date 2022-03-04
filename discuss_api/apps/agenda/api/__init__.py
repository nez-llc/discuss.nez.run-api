from ninja import Router
from . import agenda
from . import comments
from . import statistics


api = Router()
api.add_router('agendas', agenda.api)
api.add_router('agendas', comments.api)
api.add_router('statistics', statistics.api)
