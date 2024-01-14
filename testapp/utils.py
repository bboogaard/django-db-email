from typing import List, Optional

from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.core.mail.backends.base import BaseEmailBackend
from django.template.loader import render_to_string


def send_simple_mail(from_email: str, to: List[str], cc: Optional[List[str]] = None,
                     bcc: Optional[List[str]] = None, fail_silently: Optional[bool] = True,
                     connection: Optional[BaseEmailBackend] = None):
    msg = EmailMessage(
        'Note from me',
        "Hello!\n\nThis is just a simple note to let you know I'm able to send mail",
        from_email=from_email,
        to=to,
        cc=cc,
        bcc=bcc,
        connection=connection
    )
    msg.send(fail_silently)


def send_html_mail(from_email: str, to: List[str], cc: Optional[List[str]] = None,
                   bcc: Optional[List[str]] = None, fail_silently: Optional[bool] = True,
                   connection: Optional[BaseEmailBackend] = None):
    msg = EmailMultiAlternatives(
        'Note from me',
        "Hello!\n\nThis is just a simple note to let you know I'm able to send mail",
        from_email=from_email,
        to=to,
        cc=cc,
        bcc=bcc,
        connection=connection
    )
    msg.attach_alternative(render_to_string('message.html'), 'text/html')
    msg.send(fail_silently)


def send_attachment_mail(from_email: str, to: List[str], cc: Optional[List[str]] = None,
                         bcc: Optional[List[str]] = None, fail_silently: Optional[bool] = True,
                         connection: Optional[BaseEmailBackend] = None):
    msg = EmailMessage(
        'Note from me',
        "Hello!\n\nThis is just a simple note to let you know I'm able to send mail",
        from_email=from_email,
        to=to,
        cc=cc,
        bcc=bcc,
        connection=connection
    )
    msg.attach('attachment.txt', b'Foobar', 'text/plain')
    msg.send(fail_silently)
