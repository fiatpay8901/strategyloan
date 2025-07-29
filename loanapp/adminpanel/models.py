from django.db import models
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

class DepositMethod(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=[('bank', 'Bank'), ('crypto', 'Crypto'), ('gateway', 'Gateway')])
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    slug = models.SlugField(unique=True)
    gateway_details = models.CharField(max_length=255, blank=True, null=True, help_text="For gateway methods (e.g., PayPal email, CashApp tag, etc.)")

    def __str__(self):
        return self.name

class CryptoWallet(models.Model):
    method = models.OneToOneField(DepositMethod, on_delete=models.CASCADE)
    coin = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if self.address:
            qr = qrcode.make(self.address)
            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            filename = f"qr_{self.coin.lower()}_{self.method.slug}.png"
            self.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.coin} Wallet"

class BankAccount(models.Model):
    method = models.OneToOneField(DepositMethod, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100)
    account_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50)
    # Add any other fields you need

    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"

class LoanTypeSetting(models.Model):
    LOAN_TYPE_CHOICES = [
        ('personal', 'Personal Loan'),
        ('business', 'Business Loan'),
        ('investment', 'Investment Loan'),
        ('emergency', 'Emergency Loan'),
    ]
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPE_CHOICES, unique=True)
    interest_rate = models.CharField(max_length=20, default='5.99% APR')
    min_amount = models.PositiveIntegerField(default=0)
    max_amount = models.PositiveIntegerField(default=0)
    term = models.CharField(max_length=50, default='1 - 12 months')

    def __str__(self):
        return self.get_loan_type_display()

