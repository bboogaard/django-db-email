from django_webtest import WebTest
from django.contrib.auth.models import User
from django.urls import reverse


from tests.factories import EmailFactory


class TestViews(WebTest):

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_superuser('admin')

    def test_html_message(self):
        email = EmailFactory(alternatives=[('<h1>Hello</h1>', 'text/html')])
        response = self.app.get(reverse('db_email:html_message', args=[email.pk]), user=self.user)
        self.assertEqual(response.status_code, 200)
        response.mustcontain('Hello')

    def test_html_message_not_logged_in(self):
        email = EmailFactory(alternatives=[('<h1>Hello</h1>', 'text/html')])
        response = self.app.get(reverse('db_email:html_message', args=[email.pk]))
        self.assertEqual(response.status_code, 302)

    def test_html_message_permission_denied(self):
        email = EmailFactory(alternatives=[('<h1>Hello</h1>', 'text/html')])
        user = User.objects.create_user('tester')
        response = self.app.get(reverse('db_email:html_message', args=[email.pk]), user=user, expect_errors=True)
        self.assertEqual(response.status_code, 403)

    def test_html_message_not_found(self):
        response = self.app.get(reverse('db_email:html_message', args=[1]), user=self.user, expect_errors=True)
        self.assertEqual(response.status_code, 404)
