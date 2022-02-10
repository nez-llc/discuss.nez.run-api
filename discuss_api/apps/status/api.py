from ninja import Router


api = Router()


@api.get('/')
def agenda_list(request):
    return {'status': 'ok'}
