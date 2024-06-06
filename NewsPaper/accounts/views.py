from django.conf import settings
from django.core.mail import send_mail
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from news.models import Author
import logging

logger = logging.getLogger(__name__)


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    template_name = 'accounts/signup.html'
    success_url = '/'

    def form_valid(self, form):
        logger.info('Form is valid')
        response = super().form_valid(form)
        user = self.object
        self.send_welcome_email(user)
        return response

    @staticmethod
    def send_welcome_email(user):
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


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
        Author.objects.create(user=user)
    return redirect('/')
