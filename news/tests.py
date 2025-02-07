from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from news.models import NewspaperIssue

class AccessControlTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.news = NewspaperIssue.objects.create(title="Test News", content="Test content")



    def test_create_news_requires_login(self):

        url = reverse('create_news')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('custom-login'), response.url)

    def test_create_news_access_logged_in_without_permission(self):
        self.client.login(username='testuser', password='password123')
        url = reverse('create_news')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

