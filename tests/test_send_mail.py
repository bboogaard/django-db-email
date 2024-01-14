import os
import shutil

from db_email.models import Email
from django.conf import settings
from django.core import mail
from django.core.validators import ValidationError
from django.test.testcases import TestCase

from testapp import utils


class TestSendMail(TestCase):

    def setUp(self):
        super().setUp()
        self.connection = mail.get_connection('db_email.backend.EmailBackend')

    def tearDown(self):
        super().tearDown()
        if os.path.exists(os.path.join(settings.MEDIA_ROOT, 'db_email')):
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'db_email'))

    def test_send_mail(self):
        utils.send_simple_mail(
            settings.FROM_EMAIL,
            ['johndoe@example.com', 'Jane Doe <janedoe@example.com>'],
            ['johnjr@example.com', 'Jane Jr <janejr@example.com>'],
            connection=self.connection
        )
        email = Email.objects.first()
        self.assertIsNotNone(email)
        self.assertEqual(email.subject, 'Note from me')
        self.assertEqual(email.body, "Hello!\n\nThis is just a simple note to let you know I'm able to send mail")
        self.assertEqual(email.from_email, settings.FROM_EMAIL)
        self.assertEqual(email.to, ['johndoe@example.com', 'Jane Doe <janedoe@example.com>'])
        self.assertEqual(email.cc, ['johnjr@example.com', 'Jane Jr <janejr@example.com>'])

    def test_send_html_mail(self):
        utils.send_html_mail(
            settings.FROM_EMAIL,
            ['johndoe@example.com', 'Jane Doe <janedoe@example.com>'],
            ['johnjr@example.com', 'Jane Jr <janejr@example.com>'],
            connection=self.connection
        )
        email = Email.objects.first()
        self.assertIsNotNone(email)
        self.assertIn("Hello", email.html)
        self.assertIn("This is just a simple note to let you know I'm able to send mail", email.html)

    def test_send_attachment_mail(self):
        utils.send_attachment_mail(
            settings.FROM_EMAIL,
            ['johndoe@example.com', 'Jane Doe <janedoe@example.com>'],
            ['johnjr@example.com', 'Jane Jr <janejr@example.com>'],
            connection=self.connection
        )
        email = Email.objects.first()
        self.assertIsNotNone(email)
        self.assertEqual(email.attachments.count(), 1)

    def test_send_mail_invalid_addresses(self):
        with self.assertRaises(ValidationError):
            utils.send_simple_mail(
                settings.FROM_EMAIL,
                ['johndoe@example', 'Jane Doe <janedoe@example.com>'],
                ['johnjr@example.com', 'Jane Jr <janejr@example.com>'],
                connection=self.connection,
                fail_silently=False
            )
