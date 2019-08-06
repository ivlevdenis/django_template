from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.conf import settings

from apps import app


@app.task
def send_templated_email(subject, to_email, template_name, **kwargs):
    html = get_template(template_name).render(kwargs)
    email = EmailMessage(subject, html, to=[to_email])
    email.content_subtype = 'html'
    email.send()
