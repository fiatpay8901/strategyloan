from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user.views import CustomDisable2FAView, CustomSetup2FAView, CustomTwoFactorLoginView

SESSION_COOKIE_SECURE = False  # for local dev
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls', namespace='user')),
    path('adminpanel/', include('adminpanel.urls', namespace='adminpanel')),
    path('', include('core.urls')),

    path('account/two_factor/disable/', CustomDisable2FAView.as_view(), name='two_factor:disable'),
    path('account/two_factor/setup/', CustomSetup2FAView.as_view(), name='two_factor:setup'),
    path('account/two_factor/', include('two_factor.urls', 'two_factor')),  # Modified line
    path('account/two_factor/login/', CustomTwoFactorLoginView.as_view(), name='two_factor:login'),

    # Allauth URLs
    # path('accounts/social/signup/', CustomSocialSignupView.as_view(), name='socialaccount_signup'),
    path('accounts/', include('allauth.urls')),
]

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns = (core + profile + plugin_urlpatterns, 'two_factor')