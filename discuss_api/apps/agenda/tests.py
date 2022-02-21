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
        profile = UserProfile.objects.create(user=user, nickname=user.username)

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
        response = client.get('/api/agendas/1', content_type='application/json')
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data['id'], 1)
        self.assertEqual(data['title'], SAMPLE_AGENDA_DATA['title'])
        self.assertEqual(data['summary'], SAMPLE_AGENDA_DATA['summary'])
        self.assertEqual(data['desc'], SAMPLE_AGENDA_DATA['desc'])

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

        self.assertEqual(data[0]['id'], 1)
        self.assertEqual(data[0]['title'], SAMPLE_AGENDA_DATA['title'])
        self.assertEqual(data[0]['tags'][0]['name'], SAMPLE_TAGS[0]['name'])

    def test_comment_list(self):
        user = User.objects.create(username='comment_tester')

        agenda = self.agenda
        agenda.insert_comment(user, '우와아아아앙ㅇ')

        client = Client()

        response = client.get('/api/agendas/1/comments', content_type='application/json')

        self.assertEqual(response.status_code, 200)
