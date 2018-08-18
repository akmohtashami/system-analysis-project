from django.core.mail import send_mail

from proxypay.settings import EMAIL_HOST_USER


def send_email(subject, content, receivers):
    receivers_email = [user.email for user in receivers]
    return send_mail(subject, content, EMAIL_HOST_USER, receivers_email)
