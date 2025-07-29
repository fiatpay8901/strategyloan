from django.contrib import admin
from .models import DepositMethod, CryptoWallet, BankAccount

@admin.register(CryptoWallet)
class CryptoWalletAdmin(admin.ModelAdmin):
    list_display = ['coin', 'address', 'method']  # <-- Use the correct field names

@admin.register(DepositMethod)
class DepositMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'status', 'slug', 'gateway_details']
    fieldsets = (
        (None, {
            'fields': ('name', 'category', 'status', 'slug', 'gateway_details')
        }),
    )

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['bank_name', 'account_name', 'account_number', 'method']
