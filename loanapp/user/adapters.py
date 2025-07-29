from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp import devices_for_user
from django.urls import reverse
from django.contrib.auth import logout

class Enforce2FAAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return True

    def login(self, request, user):
        # Only enforce 2FA if this is a social login and NOT admin
        if request.session.get('socialaccount_sociallogin') and not request.path.startswith('/admin/'):
            if TOTPDevice.objects.filter(user=user, confirmed=True).exists():
                logout(request)
                request.session['require_2fa'] = True
        # Remove password check for social users
        return super().login(request, user)

    def get_login_redirect_url(self, request):
        # Only redirect if not admin
        if request.session.pop('require_2fa', False) and not request.path.startswith('/admin/'):
            user = request.user
            # Remove password reset redirect for social users
            return '/user/login/?next=/user/dashboard/'
        return super().get_login_redirect_url(request)

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        if user.pk and self._has_2fa_enabled(user):
            # Mark session for 2FA enforcement
            request.session['social_login_2fa_user_id'] = user.pk
            request.session['social_login_2fa_backend'] = sociallogin.account.provider

    def get_login_redirect_url(self, request):
        # If this is a social login and user has 2FA, force redirect to 2FA login page
        if request.session.pop('social_login_2fa_user_id', None):
            return reverse('two_factor:login')
        return super().get_login_redirect_url(request)

    def authentication_error(self, request, provider_id, error=None, exception=None, extra_context=None):
        if 'social_login_2fa_user_id' in request.session:
            del request.session['social_login_2fa_user_id']
        if 'social_login_2fa_backend' in request.session:
            del request.session['social_login_2fa_backend']
        return super().authentication_error(request, provider_id, error, exception, extra_context)

    def _has_2fa_enabled(self, user):
        return (devices_for_user(user) or 
                TOTPDevice.objects.filter(user=user, confirmed=True).exists())

    def get_connect_redirect_url(self, request, socialaccount):
        if 'social_login_2fa_user_id' in request.session:
            return reverse('two_factor:login')
        return super().get_connect_redirect_url(request, socialaccount)