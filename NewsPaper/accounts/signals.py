from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@receiver(user_signed_up)
def send_welcome_email(request, user, **kwargs):
    subject = 'Добро пожаловать на наш сайт, рады вас приветствовать!'
    message = 'Спасибо за регистрацию'
    recipient_list = [user.email]

    logger.info(f'Sending welcome email to {user.email}')
    logger.info(f'Subject: {subject}')
    logger.info(f'Message: {message}')

    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        logger.info(f'Welcome email sent to {user.email}')
    except Exception as e:
        logger.error(f'Error sending welcome email to {user.email}: {e}')


