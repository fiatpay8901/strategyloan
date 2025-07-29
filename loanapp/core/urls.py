from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
     path('terms/', views.terms, name='terms'),
    path('faq/', views.faq, name='faq'),
    path('privacy/', views.privacy, name='privacy'),
    path('business-loan/', views.business_loan, name='business_loan'),
    path('investment-loan/', views.investment_loan, name='investment_loan'),
    path('personal-loan/', views.personal_loan, name='personal_loan'),
    path('emergency-loan/', views.emergency_loan, name='emergency_loan'),
]
