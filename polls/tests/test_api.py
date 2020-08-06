from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User

from polls.models import Poll, Choice


class PollsAPITests(APITestCase):

    fixtures = ['auth.json', 'polls.json', 'authtoken.json']

    url = reverse('polls:poll-list')

    def setUp(self):
        super().setUp()

    def test_polls_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_polls_count(self):
        count = Poll.objects.count()
        response = self.client.get(self.url)
        self.assertEqual(count, len(response.json()))

    def test_create_polls_annonimous(self):
        data = {"name": "name", "text": "text"}
        response = self.client.post(self.url, data=data)
        self.assertEqual(401, response.status_code)

    def test_create_polls_admin(self):
        data = {"name": "name", "text": "text"}
        user = User.objects.get(username='pollsadmin')
        client = APIClient()
        client.force_authenticate(user=user, token=user.auth_token)
        response = client.post(self.url, data=data)
        self.assertEqual(201, response.status_code)

    def test_change_polls_admin(self):
        user = User.objects.get(username='pollsadmin')
        client = APIClient()
        client.force_authenticate(user=user, token=user.auth_token)

        poll = Poll.objects.last()
        url = reverse('polls:poll-detail', args=[poll.id])
        data = {"name": "name changed", "text": "text changed"}
        response = client.patch(url, data=data)
        self.assertEqual(200, response.status_code)

    def test_change_polls_date(self):
        user = User.objects.get(username='pollsadmin')
        client = APIClient()
        client.force_authenticate(user=user, token=user.auth_token)

        poll = Poll.objects.last()
        url = reverse('polls:poll-detail', args=[poll.id])
        data = {"date_start": "2020-08-01"}

        response = client.patch(url, data, format='json')
        self.assertEqual(400, response.status_code)

    def test_change_polls_admin_related(self):
        poll = Poll.objects.first()
        url = reverse('polls:poll-detail', args=[poll.id])
        data = {
            "questions": [
                {   
                    "id": "1",
                    "text": "Select new"
                },
                {
                    "text": "New created",
                    "question_type": "TEXT"
                }
            ]
        }
        user = User.objects.get(username='pollsadmin')
        client = APIClient()
        client.force_authenticate(user=user, token=user.auth_token)
        response = client.patch(url, data, format='json')
        self.assertEqual(200, response.status_code)


class ChoiceAPITest(APITestCase):

    fixtures = ['auth.json', 'polls.json', 'authtoken.json']

    url = reverse('polls:choice-list')
    poll = Poll.objects.first()
    questionvote = poll.questions.first().questionvotes.first()

    def test_add_choice_anonimously(self):
        data = {
            "author": 111,
            "questionvote": self.questionvote.id,
            "vote": True
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(201, response.status_code)

    def test_filter_choices(self):
        filter_url = reverse('polls:choice-list') + "?author=777"
        data = {
            "author": 777,
            "questionvote": self.questionvote.id,
            "vote": True
        }
        self.client.post(self.url, data, format='json')
        data = {
            "author": 1000,
            "questionvote": self.questionvote.id,
            "vote": True
        }
        self.client.post(self.url, data, format='json')
        self.assertEqual(4, Choice.objects.count())
        response = self.client.get(filter_url)
        self.assertEqual(1, len(response.json()))
