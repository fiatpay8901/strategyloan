from django.contrib import admin
from .models import UserProfile, LoanApplication, DepositTransaction

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'next_repayment', 'balance', 'active_loan', 'currency', 'loan_status')
    search_fields = ('user__username',)
    list_editable = ('balance', 'active_loan', 'currency', 'loan_status')
    fields = ('user', 'next_repayment', 'balance', 'active_loan', 'currency', 'loan_status')

@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'loan_amount', 'loan_currency', 'loan_term', 'status', 'submitted_at')
    search_fields = ('user__username', 'loan_purpose', 'loan_currency')
    list_filter = ('status', 'loan_currency', 'submitted_at')

@admin.register(DepositTransaction)
class DepositTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'method', 'status', 'submitted_at', 'reviewed_at']
    list_filter = ['status', 'method']
    actions = ['approve_deposits', 'reject_deposits']

    def approve_deposits(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='approved')
        self.message_user(request, f"{updated} deposit(s) approved.")

    approve_deposits.short_description = "Approve selected deposits"

    def reject_deposits(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='rejected')
        self.message_user(request, f"{updated} deposit(s) rejected.")

    reject_deposits.short_description = "Reject selected deposits"
