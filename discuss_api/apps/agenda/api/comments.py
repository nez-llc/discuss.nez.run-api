from ninja import Router

from discuss_api.apps.agenda.models import Comment
from discuss_api.apps.agenda.schema import CommentOut


api = Router()


@api.get('/{agenda_id}/comments', response=list[CommentOut])
def comment_list(request, agenda_id: int):
    comments = Comment.objects.filter(agenda__pk=agenda_id)
    return comments
