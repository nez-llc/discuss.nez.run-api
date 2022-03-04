from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError

from discuss_api.apps.agenda.models import Comment, Agenda
from discuss_api.apps.agenda.schema import CommentOut, CommentIn
from discuss_api.apps.member.auth import TokenAuth

api = Router()


@api.get('/{agenda_id}/comments', response=list[CommentOut])
def comment_list(request, agenda_id: int):
    comments = Comment.objects.filter(agenda__id=agenda_id)
    return comments


@api.post('/{agenda_id}/comments', response={201: CommentOut}, auth=TokenAuth())
def insert_comment(request, agenda_id: int, comment_content: CommentIn):
    agenda = get_object_or_404(Agenda, id=agenda_id)
    comment = agenda.insert_comment(request.auth, comment_content.content)
    return comment


@api.put('/{agenda_id}/comments/{comment_id}', response={201: CommentOut}, auth=TokenAuth())
def edit_comment(request, comment_id: int, comment_content: CommentIn):
    comment = get_object_or_404(Comment, id=comment_id)

    if not request.auth:
        raise HttpError(401, 'Unauthorized')

    if request.auth != comment.writer:
        raise HttpError(403, "You don't have permission to access")

    comment.content = comment_content.content
    comment.save()
    return comment


@api.delete('/{agenda_id}/comments/{comment_id}', auth=TokenAuth())
def delete_comment(request, comment_id: int):
    Comment.objects.get(id=comment_id, writer=request.auth).delete()


@api.post('/{agenda_id}/comments/{comment_id}/agreement', response={201: int}, auth=TokenAuth())
def add_comment_agreement(request, comment_id: int):
    comment = Comment.objects.get(id=comment_id)
    comment.add_agreement(request.auth)
    return comment.agreement


@api.delete('/{agenda_id}/comments/{comment_id}/agreement', response={201: int}, auth=TokenAuth())
def delete_comment_agreement(request, comment_id: int):
    comment = Comment.objects.get(id=comment_id, writer=request.auth)
    comment.delete_agreement(request.auth)
    return comment.agreement
