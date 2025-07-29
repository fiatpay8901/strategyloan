from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from user.models import KYCSubmission, UserProfile, LoanApplication
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db import IntegrityError
from .models import DepositMethod, CryptoWallet, BankAccount
from user.models import DepositTransaction
from django.utils import timezone
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

# Import your adminpanel models
from .models import DepositMethod, CryptoWallet, LoanTypeSetting

def admin_dashboard(request):
    total_users = User.objects.count()
    total_kyc = KYCSubmission.objects.count()
    pending_kyc = KYCSubmission.objects.filter(status='pending').count()
    recent_applications = LoanApplication.objects.order_by('-submitted_at')[:10]
    deposits = DepositTransaction.objects.all().order_by('-submitted_at')

    loan_types = {}
    for loan_type, display_name in LoanTypeSetting.LOAN_TYPE_CHOICES:
        obj, _ = LoanTypeSetting.objects.get_or_create(loan_type=loan_type)
        loan_types[loan_type] = {
            'display_name': display_name,
            'interest_rate': obj.interest_rate,
            'min': obj.min_amount,
            'max': obj.max_amount,
            'term': obj.term,
        }

    context = {
        'total_users': total_users,
        'total_kyc': total_kyc,
        'pending_kyc': pending_kyc,
        'recent_applications': recent_applications,
        'deposits': deposits,
        'loan_types': loan_types,
    }
    return render(request, 'adminpanel/admin-dashboard.html', context)

@staff_member_required
def admin_user_list(request):
    users = User.objects.all()
    return render(request, 'adminpanel/admin-users.html', {'users': users})

def admin_user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    kyc = getattr(user, 'kycsubmission', None)
    profile = getattr(user, 'userprofile', None)
    user_loans = LoanApplication.objects.filter(user=user).order_by('-submitted_at')
    deposits = DepositTransaction.objects.filter(user=user).order_by('-submitted_at')

    repayment_alert = False
    if profile and getattr(profile, "repayment_alert_pending", False):
        repayment_alert = True
        profile.repayment_alert_pending = False
        profile.save()

    if request.method == 'POST':
        action = request.POST.get('action')
        loan_id = request.POST.get('loan_id')
        if action in ['approve_loan', 'reject_loan'] and loan_id:
            loan = LoanApplication.objects.get(id=loan_id)
            if action == 'approve_loan':
                loan.status = 'approved'
            elif action == 'reject_loan':
                loan.status = 'rejected'
            loan.save()
            messages.success(request, f"Loan application #{loan.id} status updated.")
            return redirect('adminpanel:admin_user_edit', user_id=user.id)
        if action == 'approve_kyc' and kyc:
            kyc.status = 'approved'
            kyc.save()
            if profile:
                profile.loan_status = 'active'
                profile.active_loan = 0.00
                profile.save()
            messages.success(request, "KYC approved successfully.")
            return redirect('adminpanel:admin_user_edit', user_id=user.id)
        elif action == 'reject_kyc' and kyc:
            kyc.status = 'rejected'
            kyc.save()
            if profile:
                profile.loan_status = 'pending'
                profile.save()
            messages.warning(request, "KYC rejected.")
            return redirect('adminpanel:admin_user_edit', user_id=user.id)
        elif action == 'save_financials' and profile:
            balance = request.POST.get('balance')
            active_loan = request.POST.get('active_loan')
            new_repayment = request.POST.get('next_repayment')
            profile.balance = balance
            profile.active_loan = active_loan
            if new_repayment:
                if str(profile.next_repayment) != new_repayment:
                    profile.next_repayment = new_repayment
                    profile.next_repayment_updated_at = timezone.now()
                    profile.repayment_alert_pending = True  # <-- Set the alert!
                    
            else:
                profile.next_repayment = None
                profile.next_repayment_updated_at = None
            profile.save()

            messages.success(request, "Financial details updated successfully.")
            return redirect('adminpanel:admin_user_edit', user_id=user.id)
        # Handle other POST actions here

        # Handle deposit approval/rejection
        deposit_id = request.POST.get('deposit_id')
        if deposit_id:
            deposit = get_object_or_404(DepositTransaction, id=deposit_id)
            if request.POST.get('action') == 'approve_deposit' and deposit.status == 'pending':
                deposit.status = 'approved'
                deposit.reviewed_at = timezone.now()
                deposit.save()
                # Optionally update user balance here
                messages.success(request, f"Deposit #{deposit.id} approved.")
            elif request.POST.get('action') == 'reject_deposit' and deposit.status == 'pending':
                deposit.status = 'rejected'
                deposit.reviewed_at = timezone.now()
                deposit.save()
                messages.warning(request, f"Deposit #{deposit.id} rejected.")
            return redirect('adminpanel:admin_user_edit', user_id=user.id)

    return render(request, 'adminpanel/admin-user-edit.html', {
        'user': user,
        'kyc': kyc,
        'profile': profile,
        'user_loans': user_loans,
        'deposits': deposits,
        'repayment_alert': repayment_alert,
    })

# Admin Payment Methods View
@staff_member_required
def manage_deposit_methods(request):
    methods = DepositMethod.objects.all()

    if request.method == 'POST':
        method_id = request.POST.get('method_id')
        name = request.POST.get('name')
        category = request.POST.get('category')
        status = request.POST.get('status')
        slug = slugify(name)

        if method_id:
            method = get_object_or_404(DepositMethod, id=method_id)
            new_slug = slugify(name)
            if DepositMethod.objects.exclude(id=method_id).filter(slug=new_slug).exists():
                messages.error(request, f"A deposit method with the name '{name}' already exists.")
                return redirect('adminpanel:manage_deposit_methods')
            method.name = name
            method.category = category
            method.status = status
            method.slug = new_slug
            if category == 'gateway':
                method.gateway_details = request.POST.get('gateway_info', '')
            method.save()
            messages.success(request, 'Deposit method updated.')
        else:
            if DepositMethod.objects.filter(slug=slug).exists():
                messages.error(request, f"A deposit method with the name '{name}' already exists.")
                return redirect('adminpanel:manage_deposit_methods')
            try:
                gateway_details = request.POST.get('gateway_info', '') if category == 'gateway' else ''
                method = DepositMethod.objects.create(
                    name=name,
                    category=category,
                    status=status,
                    slug=slug,
                    gateway_details=gateway_details
                )
                messages.success(request, 'Deposit method added.')
            except IntegrityError:
                messages.error(request, "A deposit method with this slug already exists.")
                return redirect('adminpanel:manage_deposit_methods')

        # Save extra details for each type
        if category == 'crypto':
            coin = request.POST.get('coin_name')
            address = request.POST.get('wallet_address')
            if coin and address:
                crypto_wallet, created = CryptoWallet.objects.get_or_create(method=method)
                crypto_wallet.coin = coin
                crypto_wallet.address = address
                crypto_wallet.save()
        elif category == 'bank':
            bank_name = request.POST.get('bank_name')
            account_name = request.POST.get('account_name')
            account_number = request.POST.get('account_number')
            if bank_name and account_name and account_number:
                bank_account, created = BankAccount.objects.get_or_create(method=method)
                bank_account.bank_name = bank_name
                bank_account.account_name = account_name
                bank_account.account_number = account_number
                bank_account.save()

        return redirect('adminpanel:manage_deposit_methods')

    return render(request, 'adminpanel/manage_deposit_methods.html', {
        'methods': methods,
    })

@staff_member_required
def delete_deposit_method(request, method_id):
    method = get_object_or_404(DepositMethod, pk=method_id)
    method.delete()
    messages.success(request, f"{method.name} deleted.")
    return redirect('adminpanel:manage_deposit_methods')

def admin_payment_methods(request):
    # Placeholder context, add real data as needed
    return render(request, 'adminpanel/admin-payment-methods.html')

# Loan Approvals View
def loan_approvals(request):
    # Placeholder context, add real data as needed
    return render(request, 'adminpanel/loan-approvals.html')

def loan_applications(request):
    applications = LoanApplication.objects.all().order_by('-submitted_at')
    return render(request, 'adminpanel/loan_applications.html', {'applications': applications})

class AdminLoginView(LoginView):
    template_name = 'adminpanel/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('adminpanel:admin_dashboard')

@staff_member_required
def edit_loan_types(request):
    if request.method == 'POST':
        for loan_type in ['personal', 'business', 'investment', 'emergency']:
            obj, _ = LoanTypeSetting.objects.get_or_create(loan_type=loan_type)
            obj.interest_rate = request.POST.get(f"{loan_type}_interest_rate", obj.interest_rate)
            obj.min_amount = request.POST.get(f"{loan_type}_min", obj.min_amount)
            obj.max_amount = request.POST.get(f"{loan_type}_max", obj.max_amount)
            obj.term = request.POST.get(f"{loan_type}_term", obj.term)
            obj.save()
        messages.success(request, "Loan type details updated successfully.")
        return redirect('adminpanel:admin_dashboard')

    # On GET, show the form with current values
    loan_types = {}
    for loan_type, display_name in LoanTypeSetting.LOAN_TYPE_CHOICES:
        obj, _ = LoanTypeSetting.objects.get_or_create(loan_type=loan_type)
        loan_types[loan_type] = {
            'display_name': display_name,
            'interest_rate': obj.interest_rate,
            'min': obj.min_amount,
            'max': obj.max_amount,
            'term': obj.term,
        }
    return render(request, 'adminpanel/admin-dashboard.html', {'loan_types': loan_types})
