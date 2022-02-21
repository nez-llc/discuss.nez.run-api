from ninja import Router
from . import agenda
from . import comments


api = Router()
api.add_router('/', agenda.api)
api.add_router('/', comments.api)
