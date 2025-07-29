from django.db import models
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from adminpanel.models import DepositMethod, CryptoWallet, BankAccount
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

User = get_user_model()



# 4. Deposit Transaction
class DepositTransaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    method = models.ForeignKey(DepositMethod, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bank_option = models.ForeignKey(BankAccount, on_delete=models.SET_NULL, null=True, blank=True)
    crypto_option = models.ForeignKey(CryptoWallet, on_delete=models.SET_NULL, null=True, blank=True)
    proof = models.FileField(upload_to='deposit_proofs/', null=True, blank=True)
    reference = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Deposit #{self.id} by {self.user.username} - {self.status}"


class LoanApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    country = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    taxpayer_id = models.CharField(max_length=100)
    employment_status = models.CharField(max_length=100)
    employer_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2)
    income_source = models.CharField(max_length=100)
    loan_purpose = models.CharField(max_length=100)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    loan_currency = models.CharField(max_length=10)
    loan_term = models.CharField(max_length=50)
    repayment_plan = models.CharField(max_length=50)
    existing_loan = models.BooleanField(default=False)
    collateral_type = models.CharField(max_length=50)
    collateral_amount = models.DecimalField(max_digits=10, decimal_places=4)
    wallet_address = models.CharField(max_length=200)
    agree_terms = models.BooleanField(default=False)
    confirm_info_accuracy = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='review')

    def __str__(self):
        return f"{self.user.username} Loan Application"



class KYCSubmission(models.Model):
    STEP_CHOICES = [
        ('address', 'Address'),
        ('identity', 'Identity'),
        ('review', 'Review'),
        ('submitted', 'Submitted'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Step 1 - Address
    full_name = models.CharField(max_length=255)  
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = CountryField(default='US')
    address_doc_type = models.CharField(max_length=50)
    address_proof = models.FileField(upload_to='kyc/address_proof/')

    # Step 2 - Identity
    id_type = models.CharField(max_length=50, blank=True, null=True)
    id_number = models.CharField(max_length=100, blank=True, null=True)
    id_document = models.FileField(upload_to='kyc/id_document/', blank=True, null=True)

    # Step 3 - Status
    current_step = models.CharField(max_length=20, choices=STEP_CHOICES, default='address')
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')  # pending, approved, rejected

    # Additional field for KYC verification alert dismissal
    kyc_verified_alert_dismissed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - KYC"

class UserProfile(models.Model):

    LOAN_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('closed', 'Closed'),
    ]
    loan_status = models.CharField(max_length=10, choices=LOAN_STATUS_CHOICES, default='pending')

    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'Pound Sterling'),
    ]

    CURRENCY_SYMBOLS = {
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
    }

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    active_loan = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default='USD')
    country = models.CharField(max_length=50, blank=True, null=True)
    next_repayment = models.DateField(null=True, blank=True)  # or DateTimeField if you want time
    repayment_alert_pending = models.BooleanField(default=False)

    # Additional fields for email verification
    email_verification_token = models.CharField(max_length=64, null=True, blank=True)
    pending_email = models.EmailField(null=True, blank=True)

    # Additional field for 2FA alert dismissal
    twofa_alert_dismissed_until = models.DateTimeField(null=True, blank=True)

    @property
    def currency_symbol(self):
        return self.CURRENCY_SYMBOLS.get(self.currency, '')

    def __str__(self):
        return self.user.username

    # Additional fields for user preferences
    language = models.CharField(max_length=30, default='English (United States)')
    timezone = models.CharField(max_length=50, default='(GMT-06:00) Central America')
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)


class LoginActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)
