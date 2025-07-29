from django.urls import path
from . import views
from .views import AdminLoginView
from django.contrib.auth.views import LogoutView

app_name = 'adminpanel'

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('users/', views.admin_user_list, name='admin_user_list'),
    path('users/<int:user_id>/edit/', views.admin_user_edit, name='admin_user_edit'),
    path('payment-methods/', views.admin_payment_methods, name='admin_payment_methods'),
    path('loan-approvals/', views.loan_approvals, name='loan_approvals'),
    path('loan-applications/', views.loan_applications, name='loan_applications'),
    path('deposit-methods/', views.manage_deposit_methods, name='manage_deposit_methods'),
    path('deposit-methods/delete/<int:method_id>/', views.delete_deposit_method, name='delete_deposit_method'),
    path('login/', AdminLoginView.as_view(), name='admin_login'),
    path('logout/', LogoutView.as_view(next_page='adminpanel:admin_login'), name='admin_logout'),
    path('edit-loan-types/', views.edit_loan_types, name='edit_loan_types'),
]
