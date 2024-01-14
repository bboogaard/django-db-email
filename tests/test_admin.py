from io import BytesIO

from db_email.admin import EmailAdmin
from db_email.models import Email
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.test import RequestFactory
from django.test.testcases import TestCase

from tests.factories import EmailFactory


class TestEmailAdmin(TestCase):

    def setUp(self):
        super().setUp()
        self.site = AdminSite()
        self.user = User.objects.create_superuser('admin')
        self.request_factory = RequestFactory()

    def test_changeview(self):
        email = EmailFactory()
        request = self.request_factory.get('/')
        request.user = self.user
        ma = EmailAdmin(Email, self.site)
        response = ma.change_view(request, str(email.pk))
        response.render()
        self.assertEqual(response.status_code, 200)

    def test_changeview_with_alternative(self):
        email = EmailFactory(alternatives=[('<h1>Hello</h1>', 'text/html')])
        request = self.request_factory.get('/')
        request.user = self.user
        ma = EmailAdmin(Email, self.site)
        response = ma.change_view(request, str(email.pk))
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertIn('View html message', response.content.decode())

    def test_changeview_with_attachment(self):
        fh = BytesIO(b'Foobar')
        email = EmailFactory(attachments=[('attachment.txt', fh, 'text/plain')])
        request = self.request_factory.get('/')
        request.user = self.user
        ma = EmailAdmin(Email, self.site)
        response = ma.change_view(request, str(email.pk))
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertIn('db_email/attachment.txt', response.content.decode())
