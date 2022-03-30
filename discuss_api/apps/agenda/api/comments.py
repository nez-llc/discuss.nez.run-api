from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError

from discuss_api.apps.agenda.models import Comment, Agenda, CommentStatus, AgreementHistory
from discuss_api.apps.agenda.schema import CommentOut, CommentIn, DeleteCommentOut, CommentAgreementOut
from discuss_api.apps.member.auth import TokenAuth


api = Router()


@api.get('/{agenda_id}/comments', response=list[CommentOut])
def comment_list(request, agenda_id: int):
    comments = Comment.objects.filter(agenda__id=agenda_id)
    return comments


@api.post('/{agenda_id}/comments', response={201: CommentOut}, auth=TokenAuth())
def insert_comment(request, agenda_id: int, comment_data: CommentIn):
    agenda = get_object_or_404(Agenda, id=agenda_id)
    comment = agenda.add_comment(request.auth, comment_data.content)
    return comment


@api.put('/{agenda_id}/comments/{comment_id}', response={201: CommentOut}, auth=TokenAuth())
def edit_comment(request, agenda_id: int, comment_id: int, comment_content: CommentIn):
    if not request.auth:
        raise HttpError(401, 'Unauthorized')

    comment = get_object_or_404(Comment, id=comment_id)
    if request.auth != comment.writer:
        raise HttpError(403, 'You don\'t have permission to access')

    comment.content = comment_content.content
    comment.save()
    return comment


@api.delete('/{agenda_id}/comments/{comment_id}', response={201: DeleteCommentOut}, auth=TokenAuth())
def delete_comment(request, agenda_id: int, comment_id: int):
    if not request.auth:
        raise HttpError(401, 'Unauthorized')

    comment = get_object_or_404(Comment, id=comment_id)
    if request.auth != comment.writer:
        raise HttpError(403, 'You don\'t have permission to access')

    comment.status = CommentStatus.DELETED_BY_USER
    comment.save()

    return 201, {'deleted_comment_id': comment.id}


@api.post('/{agenda_id}/comments/{comment_id}/agreement', response={201: CommentAgreementOut}, auth=TokenAuth())
def add_comment_agreement(request, agenda_id: int, comment_id: int):
    if not request.auth:
        raise HttpError(401, 'Unauthorized')

    comment = get_object_or_404(Comment, id=comment_id)
    comment.add_agreement(request.auth)
    return 201, {'total_agreement': comment.agreement}


@api.delete('/{agenda_id}/comments/{comment_id}/agreement', response={201: CommentAgreementOut}, auth=TokenAuth())
def delete_comment_agreement(request, agenda_id: int, comment_id: int):
    if not request.auth:
        raise HttpError(401, 'Unauthorized')

    comment = get_object_or_404(Comment, id=comment_id)
    agreement_history = get_object_or_404(AgreementHistory, comment=comment, voter=request.auth)

    if request.auth != agreement_history.voter:
        raise HttpError(403, 'You don\'t have permission to access')

    if agreement_history:
        comment.delete_agreement(request.auth)

    return 201, {'total_agreement': comment.agreement}
