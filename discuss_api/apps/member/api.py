from django.shortcuts import get_object_or_404
from ninja import File
from ninja.files import UploadedFile
from ninja import Router
from ninja.errors import HttpError

from discuss_api.apps.agenda.models import Comment, Agenda, CommentStatus
from discuss_api.apps.agenda.schema import CommentOut, AgendaOut
from discuss_api.apps.multi_auth.auth import TokenAuth
from discuss_api.apps.member.models import UserProfile, ProfilePicture
from discuss_api.apps.member.schema import UserOut, UserIn

from google.cloud import storage

api = Router()


@api.post('/files', auth=TokenAuth())
def upload(request, file: UploadedFile):
    if not request.auth:
        raise HttpError(401, '')

    storage_client = storage.Client()
    bucket = storage_client.bucket('discuss-test-static')
    blob = bucket.blob('profile-pictures/' + file.name)

    blob.upload_from_file(file.file, content_type=file.content_type)

    picture = ProfilePicture.objects.create(
        profile=request.auth.profile,
        file=blob.public_url
    )

    return {
        'file_id': picture.id,
        'url': picture.file,
    }


@api.get('/my', response={200: UserOut}, auth=TokenAuth())
def get_my_member(request):
    if not request.auth:
        raise HttpError(401, 'Unauthorized')

    return request.auth


@api.get('/my/comments', response={200: list[CommentOut]}, auth=TokenAuth())
def get_my_comments(request):
    if not request.auth:
        raise HttpError(401, 'Unauthorized')

    comments = Comment.objects.filter(writer=request.auth)
    return comments


@api.get('/my/agenda', response={200: list[AgendaOut]}, auth=TokenAuth())
def get_my_agendas(request):
    if not request.auth:
        raise HttpError(401, 'Unauthorized')

    agendas = Agenda.objects.filter(writer=request.auth)
    return agendas


@api.put('/my', response={201: UserOut}, auth=TokenAuth())
def edit_my(request, member_data: UserIn):
    profile, created = UserProfile.objects.get_or_create(user=request.auth)

    if not request.auth:
        raise HttpError(401, 'Unauthorized')

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
