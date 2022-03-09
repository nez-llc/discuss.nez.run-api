from django.contrib.auth.models import User
from django.test import TestCase, Client

from discuss_api.apps.agenda.models import Updown, Agenda
from discuss_api.apps.member.models import Token, UserProfile
from discuss_api.apps.tag.models import Tag


SAMPLE_AGENDA_DATA = {
    'title': '유잼 제목',
    'summary': '유잼 요약',
    'desc': '유잼 설명',
}

SAMPLE_TAGS = [{
    'name': '유재',
}, {
    'name': '유잼',
}]


class AgendaTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='tester')
        UserProfile.objects.create(user=user, nickname=user.username)

        self.agenda = Agenda.objects.create(
            writer=user,
            title=SAMPLE_AGENDA_DATA['title'],
            summary=SAMPLE_AGENDA_DATA['summary'],
            desc=SAMPLE_AGENDA_DATA['desc'],
        )

        for sample_tag in SAMPLE_TAGS:
            tag = Tag.objects.create(name=sample_tag['name'])
            self.agenda.tags.add(tag)

    def test_updown_model(self):
        user = User.objects.create(
            username='updown_tester',
        )

        agenda = self.agenda

        self.assertEqual(agenda.updown, {'total': 0, 'up': 0, 'down': 0})

        agenda.add_updown(user, Updown.UP)
        self.assertEqual(agenda.updown, {'total': 1, 'up': 1, 'down': 0})

        agenda.add_updown(user, Updown.UP)
        self.assertEqual(agenda.updown, {'total': 1, 'up': 1, 'down': 0})

        agenda.add_updown(user, Updown.DOWN)
        self.assertEqual(agenda.updown, {'total': -1, 'up': 0, 'down': 1})

    def test_agenda(self):
        client = Client()
        response = client.get('/api/agendas/')

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['total'], 1)
        self.assertEqual(data['per_page'], 10)
        self.assertEqual(data['current_page'], 1)

        response = client.get('/api/agendas/1', content_type='application/json')
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data['id'], 1)
        self.assertEqual(data['title'], SAMPLE_AGENDA_DATA['title'])
        self.assertEqual(data['summary'], SAMPLE_AGENDA_DATA['summary'])
        self.assertEqual(data['desc'], SAMPLE_AGENDA_DATA['desc'])
        self.assertEqual(data['updown'], {'total': 0, 'up': 0, 'down': 0})
        self.assertEqual(data['vote_count'], {'agree': 0, 'not_agree': 0, 'not_sure': 0})

    def test_agenda_update(self):
        writer = User.objects.create(username='agendaAPI_tester')
        other_user = User.objects.create(username='agendaAPI_tester2')

        token_for_writer = Token.objects.create(user=writer, value='s4mp13_t0k3n')
        token_for_other = Token.objects.create(user=other_user, value='0th3r_t0k3n')

        updated_values = {
            'title': 'Updated title',
            'summary': 'Updated summary',
            'desc': 'Updated desc',
        }

        authorized_headers = {
            'HTTP_AUTHORIZATION': f'Bearer {token_for_writer.value}'
        }

        client = Client()

        response = client.post('/api/agendas/', {
            'title': 'New title',
            'summary': 'New summary',
            'desc': 'New desc',
        }, content_type='application/json', **authorized_headers)
        self.assertEqual(response.status_code, 201)

        # Unauthorized request
        response = client.post('/api/agendas/1', updated_values)
        self.assertEqual(response.status_code, 401)

        # request from not the owner of the post
        response = client.post('/api/agendas/1', updated_values, content_type='application/json',
                               **{'HTTP_AUTHORIZATION': f'Bearer {token_for_other.value}'})
        self.assertEqual(response.status_code, 403)

        # request to not exists
        response = client.post('/api/agendas/999',
                               updated_values, content_type='application/json', **authorized_headers)
        self.assertEqual(response.status_code, 404)

        response = client.post('/api/agendas/1', {
            'title': '',
            # missing desc
        }, **authorized_headers)
        self.assertEqual(response.status_code, 400)

    def test_agenda_updown(self):
        user = User.objects.create(username='updownAPI_tester')

        token = Token.objects.create(user=user, value='s4mp13_t0k3n')

        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {token.value}'
        }

        client = Client()

        response = client.get('/api/agendas/1', content_type='application/json')
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data['updown'], {
            'total': 0,
            'up': 0,
            'down': 0,
        })

        response = client.post('/api/agendas/1/updown', {
            'updown': Updown.UP,
        }, content_type='application/json', **headers)

        data = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {
            'total': 1,
            'up': 1,
            'down': 0,
        })

    def test_agenda_tags(self):
        client = Client()
        response = client.get('/api/agendas/1', content_type='application/json')
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data['tags'][0]['name'], SAMPLE_TAGS[0]['name'])

    def test_agendas_of_tag(self):
        client = Client()
        response = client.get('/api/agendas/?tag=유재', content_type='application/json')
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data['items'][0]['id'], 1)
        self.assertEqual(data['items'][0]['title'], SAMPLE_AGENDA_DATA['title'])
        self.assertEqual(data['items'][0]['tags'][0]['name'], SAMPLE_TAGS[0]['name'])

    def test_comment_list(self):
        user = User.objects.create(username='comment_reader')

        agenda = self.agenda
        agenda.add_comment(user, '우와아아아앙ㅇ')

        client = Client()

        response = client.get('/api/agendas/1/comments', content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_comment(self):
        user = User.objects.create(username='commentAPI_writer')

        token = Token.objects.create(user=user, value='s4mp13_t0k3n')

        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {token.value}'
        }

        client = Client()
        response = client.post('/api/agendas/1/comments', {
            'content': 'Okay',
        }, content_type='application/json', **headers)

        self.assertEqual(response.status_code, 201)

        response = client.post('/api/agendas/1/comments', {
            'content': '정책 토론을 위한 댓글 등록 테스트 코드이다. Test content for discuss agenda service~ insert new comment',
        }, content_type='application/json', **headers)
        self.assertEqual(response.status_code, 201)

        # Unauthorized request
        response = client.put('/api/agendas/1/comments/1', {
            'content': 'I change my mind, I think is not okay!',
        }, content_type='application/json')
        self.assertEqual(response.status_code, 401)

        response = client.put('/api/agendas/1/comments/1', {
            'content': 'I change my mind, I think is not okay!',
        }, content_type='application/json', **headers)

        self.assertEqual(response.status_code, 201)

        other_user = User.objects.create(username='commentAPI_another_tester')
        token_for_other = Token.objects.create(user=other_user, value='0th3r_t0k3n')

        # request from not the owner of the comment
        response = client.put('/api/agendas/1/comments/1', {
            'content': 'I think is not okay!',
        }, content_type='application/json', **{
            'HTTP_AUTHORIZATION': f'Bearer {token_for_other.value}'
        })
        self.assertEqual(response.status_code, 403)

        response = client.delete('/api/agendas/1/comments/2', **headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), 2)

    def test_comment_agreement(self):
        user = User.objects.create(username='commentAPI_agreement_user')

        token = Token.objects.create(user=user, value='s4mp13_t0k3n')

        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {token.value}'
        }

        client = Client()
        response = client.post('/api/agendas/1/comments', {
            'content': 'Good Comment~~',
        }, content_type='application/json', **headers)
        self.assertEqual(response.status_code, 201)

        response = client.post('/api/agendas/1/comments/1/agreement', **headers)
        self.assertEqual(response.status_code, 201)

        response = client.delete('/api/agendas/1/comments/1/agreement', **headers)
        self.assertEqual(response.status_code, 201)

        response = client.delete('/api/agendas/1/comments/2/agreement', **headers)
        self.assertEqual(response.status_code, 404)

        other_user = User.objects.create(username='agreementAPI_another_tester')
        token_for_other = Token.objects.create(user=other_user, value='0th3r_t0k3n')

        # request from not the owner of the comment
        response = client.delete('/api/agendas/1/comments/1/agreement', **{
            'HTTP_AUTHORIZATION': f'Bearer {token_for_other.value}'
        })
        self.assertEqual(response.status_code, 404)

    def test_vote(self):
        user = User.objects.create(username='voteAPI_voter')
        token = Token.objects.create(user=user, value='s4mp13_t0k3n')
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {token.value}'
        }

        client = Client()
        response = client.post('/api/agendas/1/votes', {
            'ballot': 'not_sure',
        }, content_type='application/json', **headers)
        self.assertEqual(response.status_code, 201)

        response = client.post('/api/agendas/1/votes', {
            'ballot': 'agree',
        }, content_type='application/json', **headers)
        self.assertEqual(response.status_code, 201)

    def test_statistics(self):
        client = Client()

        response = client.get('/api/statistics/')

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['agenda_count'], 1)
        self.assertEqual(data['comment_count'], 0)
        self.assertEqual(data['vote_count'], 0)
