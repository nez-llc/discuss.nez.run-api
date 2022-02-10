from django.contrib.auth.models import User
from django.test import TestCase, Client

from discuss_api.apps.agenda.models import Updown, Agenda


SAMPLE_AGENDA_DATA = {
    'title': '유잼 제목',
    'summary': '유잼 요약',
    'desc': '유잼 설명',
}


class AgendaTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            username='tester',
        )

        Agenda.objects.create(
            writer=user,
            title=SAMPLE_AGENDA_DATA['title'],
            summary=SAMPLE_AGENDA_DATA['summary'],
            desc=SAMPLE_AGENDA_DATA['desc'],
        )

    def test_updown_model(self):
        user = User.objects.create(
            username='updown_tester',
        )

        agenda = Agenda.objects.create(
            writer=user,
            title=SAMPLE_AGENDA_DATA['title'],
            summary=SAMPLE_AGENDA_DATA['summary'],
            desc=SAMPLE_AGENDA_DATA['desc'],
        )

        self.assertEqual(agenda.updown, {'total': 0, 'up': 0, 'down': 0})

        agenda.add_updown(user, Updown.UP)
        self.assertEqual(agenda.updown, {'total': 1, 'up': 1, 'down': 0})

        agenda.add_updown(user, Updown.UP)
        self.assertEqual(agenda.updown, {'total': 1, 'up': 1, 'down': 0})

        agenda.add_updown(user, Updown.DOWN)
        self.assertEqual(agenda.updown, {'total': -1, 'up': 0, 'down': 1})

    def test_agenda(self):
        client = Client()
        response = client.get('/api/agendas/1/', content_type='application/json')
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data['id'], 1)
        self.assertEqual(data['title'], SAMPLE_AGENDA_DATA['title'])
        self.assertEqual(data['summary'], SAMPLE_AGENDA_DATA['summary'])
        self.assertEqual(data['desc'], SAMPLE_AGENDA_DATA['desc'])

    def test_agenda_updown(self):
        client = Client()
        response = client.get('/api/agendas/1/', content_type='application/json')
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data['updown'], {
            'point': 0,
            'up': 0,
            'down': 0,
        })

        response = client.post('/api/agendas/1/updown/', {
            'updown': Updown.UP,
        }, content_type='application/json')
        data = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {
            'point': 1,
            'up': 1,
            'down': 0,
        })
