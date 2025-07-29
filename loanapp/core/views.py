from django.shortcuts import render
from django.urls import path
from . import views
from django.templatetags.static import static


def home(request):

    approved_logos = [
        {"name": "Boa", "url": static("assets/images/approved/bank-of-america.svg")},
        {"name": "chase", "url": static("assets/images/approved/chase.svg")},
        {"name": "chase", "url": static("assets/images/approved/logo_1.svg")},
        {"name": "chase", "url": static("assets/images/approved/logo_2.svg")},
        {"name": "chase", "url": static("assets/images/approved/logo_3.svg")},
        {"name": "chase", "url": static("assets/images/approved/logo_4.svg")},
        {"name": "chase", "url": static("assets/images/approved/logo_5.svg")},
        {"name": "chase", "url": static("assets/images/approved/td-bank-1.svg")},
        {"name": "chase", "url": static("assets/images/approved/citizens-bank-logo-1.svg")},
    ]

    return render(request, 'core/home.html', {"approved_logos": approved_logos})

def services(request):
    return render(request, 'core/services.html')



def contact(request):
    return render(request, 'core/contact.html')

def terms(request):
    return render(request, 'core/terms.html')


def faq(request):
    return render(request, 'core/faq.html')

def privacy(request):
    return render(request, 'core/privacy.html')

def business_loan(request):
    return render(request, 'core/businessloan.html')

def investment_loan(request):
    return render(request, 'core/investmentloan.html')

def personal_loan(request):
    return render(request, 'core/Personalloan.html')

def emergency_loan(request):
    return render(request, 'core/Emergencyloan.html')
