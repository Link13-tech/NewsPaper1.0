from allauth.account.forms import SignupForm as AccountSignupForm
from django.contrib.auth.models import Group
from allauth.socialaccount.forms import SignupForm as SocialSignupForm


class CommonSignupForm(AccountSignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user


class CommonSocSignupForm(SocialSignupForm):
    def save(self, request):
        user = super(CommonSocSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
