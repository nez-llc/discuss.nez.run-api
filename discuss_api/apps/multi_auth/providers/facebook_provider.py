import uuid
import requests
from django.db import transaction
from discuss_api.apps.member.models import User
from discuss_api.apps.multi_auth.models import OAuth

def exchange_token(tokens):
    resp = requests.get(
        'https://graph.facebook.com/v4.0/me',
        params={
            'fields': 'id,email',
            'access_token': tokens['access_token'],
        })

    result = resp.json()

    with transaction.atomic():
        try:
            auth = OAuth.objects.get(provider='facebook', id_on_provider=result['id'])
        except OAuth.DoesNotExist:
            user = User.objects.create(email=result['email'], username=uuid.uuid4())
            auth = OAuth.objects.create(provider='facebook', id_on_provider=result['id'], user=user)

    return auth
