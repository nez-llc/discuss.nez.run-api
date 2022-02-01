from django.test import TestCase, Client


class StatusTest(TestCase):
    def test_status(self):
        client = Client()
        response = client.get('/api/status/')

        self.assertEqual(response.status_code, 200)
