from ninja import Router
from discuss_api.apps.tag.models import Tag

api = Router()


@api.get('/')
def tag_list(request):
    q = Tag.objects.all()

    return list(q.values())
