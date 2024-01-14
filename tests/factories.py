import factory

from db_email import models
from django.conf import settings


class EmailFactory(factory.django.DjangoModelFactory):

    subject = 'Note from me'

    body = "Hello!\n\nThis is just a simple note to let you know I'm able to send mail"

    from_email = settings.FROM_EMAIL

    to = ['johndoe@example.com', 'Jane Doe <janedoe@example.com>']

    cc = ['johnjr@example.com', 'Jane Jr <janejr@example.com>']

    class Meta:
        model = models.Email
        skip_postgeneration_save = True

    @factory.post_generation
    def alternatives(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for content, mimetype in extracted:
                models.EmailAlternative.objects.create(
                    email=self,
                    content=content,
                    mimetype=mimetype
                )

    @factory.post_generation
    def attachments(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for filename, fh, mimetype in extracted:
                attachment = models.EmailAttachment.objects.create(
                    email=self,
                    mimetype=mimetype
                )
                attachment.file.save(filename, fh)
