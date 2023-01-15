from ninja import Router, Schema

from discuss_api.apps.multi_auth.models import OAuth
from discuss_api.apps.multi_auth.providers import (
    twitter_provider,
    facebook_provider,
    github_prodiver,
)
from discuss_api.apps.member.models import User, UserProfile


providers = {
    'twitter': twitter_provider,
    'facebook': facebook_provider,
    'github': github_prodiver,
}

api = Router()


class TokenRequest(Schema):
    provider: str
    tokens: dict


@api.post('/token')
def exchange_token(request, provided: TokenRequest):
    tokens = provided.tokens
    provider_id = provided.provider
    provider = providers[provider_id]

    auth = provider.exchange_token(tokens)
    token = auth.issue_token()

    print(provider)
    print(tokens)
    print(auth)
    print(token)

    # match provider:
    #     case 'twitter':
    #         # auth, created = OAuth.objects.get_or_create(provider=provider)
    #         # try:
    #         #     OAuth.objects.get(provider=provider, )
    #         # token = twitter.exchange_token(tokens)
    #         pass
    #     case 'facebook':
    #         token = facebook.exchange_token(tokens)
    #     case 'github':
    #         pass

    # print(request.body)
    # print(request.body.items())
    #
    # # if provider == 'facebook':
    # #     pass
    #
    # graph = GraphAPI(request.body['access_token'])
    # response = graph.get('/me', dict(fields='id,name,email'))
    # print(response)
    #
    # # response = graph.request('/me', dict(fields=['id', 'name', 'email']))
    #
    # facebook_id = response['id']
    #
    # auth, created = OAuth.objects.get_or_create(id=facebook_id)
    #
    # # 새로 가입한 경우
    # if created:
    #     user = User.objects.create()
    #     auth.user = user
    #     auth.save()
    #
    #     UserProfile.objects.create(
    #         user=user,
    #         nickname=response['name'],
    #     )
    #
    # token = Token.objects.create(user=auth.user)

    return {
        'token': token.value,
    }
