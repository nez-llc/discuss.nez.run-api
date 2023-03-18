from ninja import File
from ninja.files import UploadedFile
from ninja import Router
from ninja.errors import HttpError

from discuss_api.apps.agenda.models import Comment, Agenda, CommentStatus, Vote
from discuss_api.apps.agenda.schema import CommentOut, AgendaOut
from discuss_api.apps.multi_auth.auth import TokenAuth
from discuss_api.apps.member.models import UserProfile, ProfilePicture
from discuss_api.apps.member.schema import UserOut, UserIn


api = Router()


@api.post('/files', auth=TokenAuth())
def upload(request, file: UploadedFile = File(...)):
    if not request.auth:
        raise HttpError(401, '')

    picture = ProfilePicture.objects.create(
        profile=request.auth.profile,
        file=file
    )

    return {
        'file_id': picture.id,
        'url': picture.file.url,
    }


@api.get('/my', response={200: UserOut}, auth=TokenAuth())
def get_my_member(request):
    if not request.auth:
        raise HttpError(401, 'Unauthorized')

    return request.auth


@api.get('/{member_id}/comments', response={200: list[CommentOut]})
def get_user_comments(request, member_id: int):
    comments = Comment.objects.filter(writer__id=member_id).order_by('-created_time')
    return comments


@api.get('/{member_id}/votes')
def get_user_votes(request, member_id: int):
    votes = Vote.objects.filter(voter__id=member_id).order_by('-created_time').select_related('agenda')
    return [{
        'agenda': {
            'id': vote.agenda.id,
            'title': vote.agenda.title,
        },
        'vote': vote.value,
        'created_time': vote.created_time,
    } for vote in votes]


@api.get('/my/agenda', response={200: list[AgendaOut]}, auth=TokenAuth())
def get_my_agendas(request):
    if not request.auth:
        raise HttpError(401, 'Unauthorized')

    agendas = Agenda.objects.filter(writer=request.auth)
    return agendas


@api.put('/my', response={201: UserOut}, auth=TokenAuth())
def edit_my(request, member_data: UserIn):
    if not request.auth:
        raise HttpError(401, 'Unauthorized')

    profile = UserProfile.objects.get(user=request.auth)
    profile.nickname = member_data.nickname
    profile.picture_id = member_data.picture_id
    profile.save()

    return profile.user


@api.delete('/my', response={201: int}, auth=TokenAuth())
def delete_member(request):
    if not request.auth:
        raise HttpError(401, 'Unauthorized')

    member = request.auth
    member.active = False
    member.save()

    member.profile.clear_contents()

    Comment.objects.filter(writer=member).update(status=CommentStatus.DELETED_BY_WITHDRAWAL)

    return member.id
