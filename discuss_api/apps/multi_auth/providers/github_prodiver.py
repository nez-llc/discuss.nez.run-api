import uuid

from django.db import transaction

from discuss_api.apps.member.models import User
from discuss_api.apps.multi_auth.models import OAuth
import requests

def exchange_token(tokens):
    access_token = 'token ' + tokens['access_token']
    url = 'https://api.github.com/user'
    headers = {"Authorization": access_token}

    resp = requests.get(url=url, headers=headers)

    result = resp.json()

    with transaction.atomic():
        try:
            auth = OAuth.objects.get(provider='github', id_on_provider=result['id'])
        except OAuth.DoesNotExist:
            user = User.objects.create(email=result['email'], username=uuid.uuid4())
            auth = OAuth.objects.create(provider='github', id_on_provider=result['id'], user=user)

    return auth