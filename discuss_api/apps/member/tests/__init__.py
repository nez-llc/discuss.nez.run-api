from os import path
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from discuss_api.apps.member.models import UserProfile, Token


TESTS_DIR = path.dirname(__file__)

User = get_user_model()


class MemberTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='mypage_tester')
        token = Token.objects.create(user=self.user, value='s4mp13_t0k3n')
        self.authorized_headers = {
            'HTTP_AUTHORIZATION': f'Bearer {token.value}'
        }

        # Image from https://commons.wikimedia.org/wiki/File:VAN_CAT.png (CC BY-SA 4.0)
        self.file_path = path.join(TESTS_DIR, 'cat_free.jpg')

    def test_mypage(self):
        client = Client()
        response = client.get('/api/members/my', **self.authorized_headers)
        self.assertEqual(response.status_code, 200)

    def change_profile_picture(self):
        client = Client()

        file_response = client.post('/api/members/files', {
            'file': open(self.file_path, 'rb')
        }, **self.authorized_headers)

        file_id = file_response.json()['file_id']
        file_url = file_response.json()['url']

        response = client.put('/api/members/my', {
            'nickname': 'test_user_hehehehe',
            'picture_id': file_id,
        }, content_type='application/json', **self.authorized_headers)
        self.assertEqual(response.status_code, 201)

    def test_profile_crated_with_user(self):
        user = User.objects.create(username='tester')
        self.assertEqual(type(user.profile), UserProfile)
