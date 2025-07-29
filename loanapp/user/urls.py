from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from two_factor.views import LoginView
# from .views import CustomSocialSignupView


app_name = 'user'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('kyc/verify/', views.kyc_step_1, name='kyc_verify'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('repay/', views.repay, name='repay'),
    path('transactions/', views.transactions, name='transactions'),
    path('help/', views.help_center, name='help_center'),
    path('loan/apply/', views.loan_apply, name='loan_apply'),
    path('deposit/', views.deposit_view, name='deposit'),
    path('deposit/<int:pk>/', views.deposit_details_view, name='deposit_details'),
    path('kyc/', views.kyc_step_1, name='kyc_step_1'),
    path('kyc/identity/', views.kyc_step_2, name='kyc_step_2'),
    path('kyc/review/', views.kyc_step_3, name='kyc_step_3'),
    path('settings/', views.profile_settings, name='profile_settings'),
    path('notifications/', views.notifications, name='notifications'),
    path('register/', views.register, name='register'),

    path('login/', LoginView.as_view(), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dismiss-kyc-verified-alert/', views.dismiss_kyc_verified_alert, name='dismiss_kyc_verified_alert'),
    path('dismiss-twofa-alert/', views.dismiss_twofa_alert, name='dismiss_twofa_alert'),
    path('deposit/success/', views.deposit_success, name='deposit_success'),
    path('profile/', views.profile, name='profile'),

    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='user/password_change.html'
    ), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='user/password_change_done.html'
    ), name='password_change_done'),

    path('accounts/password/reset/', auth_views.PasswordResetView.as_view(
        template_name='user/password_reset.html'
    ), name='password_reset'),
    path('accounts/password/reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='user/password_reset_done.html'
    ), name='password_reset_done'),
    path('accounts/password/set/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='user/password_set.html',
        success_url='/user/login/'  # Redirect to login after setting password
    ), name='password_reset_confirm'),
    path('accounts/password/set/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='user/password_set_done.html'
    ), name='password_reset_complete'),

    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),
    path('test-disable/', views.test_disable, name='test_disable'),
    path('post-signup/', views.post_signup, name='post_signup'),

]