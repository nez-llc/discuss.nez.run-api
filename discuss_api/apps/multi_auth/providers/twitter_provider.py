import uuid

import tweepy
from django.conf import settings
from django.db import transaction

from discuss_api.apps.member.models import User
from discuss_api.apps.multi_auth.models import OAuth


def exchange_token(tokens):
    auth = tweepy.OAuthHandler(
        settings.TWITTER_CONSUMER_KEY,
        settings.TWITTER_CONSUMER_SECRET,
        tokens['oauth_token'],
        tokens['oauth_token_secret']
    )
    api = tweepy.API(auth)

    result = api.verify_credentials(
        include_entities=False,
        include_email=True,
        skip_status=True,
    )

    print(result)

    with transaction.atomic():
        try:
            auth = OAuth.objects.get(provider='twitter', id_on_provider=result.id_str)
        except OAuth.DoesNotExist:
            user = User.objects.create(email=result.email, username=uuid.uuid4())
            auth = OAuth.objects.create(provider='twitter', id_on_provider=result.id_str, user=user)

    return auth
