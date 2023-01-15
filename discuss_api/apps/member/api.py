import re
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from ninja import File
from ninja.files import UploadedFile
from ninja import Router
from ninja.errors import HttpError


from discuss_api.apps.agenda.models import Comment, Agenda, CommentStatus
from discuss_api.apps.agenda.schema import CommentOut, AgendaOut
from discuss_api.apps.multi_auth.auth import TokenAuth
from discuss_api.apps.member.models import UserProfile, ProfilePicture
from discuss_api.apps.member.schema import UserOut, UserIn, UserSignup, UserLogin
from discuss_api.apps.multi_auth.models import Token

api = Router()


@api.post('/signup')
def upload(request, user_signup: UserSignup):
    regex = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

    if regex.match(user_signup.email) is None:
        raise HttpError(400, '')

    if User.objects.filter(username=user_signup.email).exists():
        raise HttpError(423, '')

    user = User.objects.create(email=user_signup.email, username=user_signup.email, password=user_signup.password)

    profile = UserProfile.objects.create(
        user=user,
        nickname=user_signup.nickname,
    )

    token = Token.objects.create(user=user)

    return {
        'token': token.value,
    }


@api.post('/login')
def upload(request, user_login: UserLogin):
    user = get_object_or_404(User, username=user_login.email, password=user_login.password)

    token = Token.objects.create(user=user)

    return {
        'token': token.value,
    }


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
