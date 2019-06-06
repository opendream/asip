from django.core.mail import send_mail as core_send_mail
from celery.task import task

@task()
def send_mail(subject, body, from_email, recipient_list, fail_silently=False, html_message=None, *args, **kwargs):
    return core_send_mail(subject, body, from_email, recipient_list, fail_silently, html_message, *args, **kwargs)
