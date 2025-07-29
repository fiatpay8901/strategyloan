from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import views as auth_views
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from .models import KYCSubmission
from .forms import KYCAddressForm, KYCIdentityForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from .models import UserProfile
from .models import LoanApplication
import uuid
from adminpanel.models import DepositMethod, CryptoWallet, BankAccount, LoanTypeSetting
from .models import DepositTransaction
from .forms import DepositInitiateForm, DepositProofForm, UserProfileForm, UserForm
from .forms import SettingsForm
from django.utils.translation import gettext as _
from django.utils import translation
from .models import LoginActivity
from decimal import Decimal, InvalidOperation
import secrets
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from two_factor.views.profile import DisableView
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect
from datetime import timedelta
from allauth.socialaccount.views import SignupView
from two_factor.views import SetupView
from two_factor.views import LoginView
from two_factor.forms import AuthenticationTokenForm, BackupTokenForm
from .forms import CustomAuthenticationTokenForm
from django_otp.plugins.otp_totp.models import TOTPDevice


# 1. Step 1: Show deposit method form (deposit.html)
@login_required
def deposit_view(request):
    deposit_methods = DepositMethod.objects.filter(status='active')
    crypto_options = CryptoWallet.objects.filter(method__status='active', method__category='crypto')

    if request.method == 'POST':
        post_data = request.POST.copy()
        if 'amount' in post_data:
            post_data['amount'] = post_data['amount'].replace(',', '')
        form = DepositInitiateForm(
            post_data or None,
            deposit_methods=deposit_methods,
            crypto_options=crypto_options
        )
        if form.is_valid():
            method_slug = form.cleaned_data['method']
            coin_pk = form.cleaned_data.get('coin')
            amount = form.cleaned_data['amount']

            method = get_object_or_404(DepositMethod, slug=method_slug)
            reference = str(uuid.uuid4()).split("-")[0]

            transaction = DepositTransaction.objects.create(
                user=request.user,
                method=method,
                amount=amount,
                reference=reference
            )

            if method.category.lower() == 'crypto' and coin_pk:
                crypto_wallet = get_object_or_404(CryptoWallet, pk=coin_pk)
                transaction.crypto_option = crypto_wallet
                transaction.save()

            if method.category.lower() == 'bank':
                bank_option = BankAccount.objects.filter(method=method).first()
                if bank_option:
                    transaction.bank_option = bank_option
                    transaction.save()

            return redirect('user:deposit_details', pk=transaction.pk)
    else:
        form = DepositInitiateForm(deposit_methods=deposit_methods, crypto_options=crypto_options)

    return render(request, 'user/deposit.html', {
        'form': form,
        'deposit_methods': deposit_methods,
        'crypto_options': crypto_options,
    })


# 2. Step 2: Show instructions + handle proof upload (deposit-details.html)
@login_required
def deposit_details_view(request, pk):
    transaction = get_object_or_404(DepositTransaction, pk=pk, user=request.user)

    if request.method == 'POST':
        form = DepositProofForm(request.POST, request.FILES, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('user:deposit_success')
    else:
        form = DepositProofForm(instance=transaction)

    return render(request, 'user/deposit-details.html', {
        'transaction': transaction,
        'form': form
    })



@login_required
def apply_loan(request):
    if request.method == 'POST':
        # Grab fields from POST
        data = request.POST

        LoanApplication.objects.create(
            user=request.user,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            dob=data.get('dob'),
            country=data.get('country'),
            address=data.get('address'),
            email=data.get('email'),
            phone=data.get('phone'),
            taxpayer_id=data.get('taxpayer_id'),
            employment_status=data.get('employment_status'),
            employer_name=data.get('employer') or "",
            job_title=data.get('job_title') or "",
            monthly_income=data.get('monthly_income') or 0.00,
            income_source=data.get('income_source') or "",
            loan_purpose=data.get('loan_purpose'),
            loan_amount=data.get('loan_amount') or 0.00,
            loan_currency=data.get('loan_currency'),
            loan_term=data.get('loan_term'),
            repayment_plan=data.get('repayment_plan'),
            existing_loan=bool(data.get('existing_loan')),
            collateral_type=data.get('collateral'),
            collateral_amount=data.get('collateral_amount') or 0.00,
            wallet_address=data.get('collateral_wallet'),
            agree_terms=bool(data.get('agree_terms')),
            confirm_info_accuracy=bool(data.get('confirm_accuracy')),
        )
        return redirect('user:dashboard')
    return render(request, 'user/apply_loan.html')




@login_required
def kyc_step_1(request):
    # Restrict access if already submitted
    if hasattr(request.user, 'kycsubmission') and request.user.kycsubmission.current_step == 'submitted':
        messages.info(request, "Your KYC has already been submitted.")
        return redirect('user:dashboard')

    try:
        kyc = request.user.kycsubmission
    except KYCSubmission.DoesNotExist:
        kyc = KYCSubmission(user=request.user)

    if request.method == 'POST':
        form = KYCAddressForm(request.POST, request.FILES, instance=kyc)
        if form.is_valid():
            kyc = form.save(commit=False)
            kyc.user = request.user
            kyc.current_step = 'identity'
            kyc.save()
            return redirect('user:kyc_step_2')  # updated
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = KYCAddressForm(instance=kyc)

    return render(request, 'user/kyc_verify.html', {'form': form})


@login_required
def kyc_step_2(request):
    kyc = request.user.kycsubmission

    if kyc.current_step != 'identity':
        return redirect('user:kyc_step_1')  # updated
    if kyc.current_step == 'submitted':
        messages.info(request, "Your KYC has already been submitted.")
        return redirect('user:dashboard')  # updated

    if request.method == 'POST':
        form = KYCIdentityForm(request.POST, request.FILES, instance=kyc)
        if form.is_valid():
            kyc = form.save(commit=False)
            kyc.current_step = 'review'
            kyc.save()
            return redirect('user:kyc_step_3')  # updated
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = KYCIdentityForm(instance=kyc)

    return render(request, 'user/kyc2.html', {'form': form})


@login_required
def kyc_step_3(request):
    kyc = request.user.kycsubmission

    if kyc.current_step != 'review':
        return redirect('user:kyc_step_2')  # updated
    if kyc.current_step == 'submitted':
        messages.info(request, "Your KYC has already been submitted.")
        return redirect('user:dashboard')  # updated

    if request.method == 'POST':
        kyc.status = 'pending'
        kyc.current_step = 'submitted'
        kyc.save()
        messages.success(request, "KYC submitted successfully!")
        return redirect('user:dashboard')  # updated

    return render(request, 'user/kyc3.html', {'kyc': kyc})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
                is_active=False
            )
            # Wait for the signal to create the profile, then update it
            profile = user.userprofile
            profile.currency = form.cleaned_data['currency']
            profile.email_verification_token = secrets.token_urlsafe(32)
            profile.save()
            # Send verification email
            token = profile.email_verification_token
            verification_url = request.build_absolute_uri(
                reverse('user:verify_email', args=[token])
            )
            send_mail(
                subject="Verify your email address",
                message=f"Click the link to verify your email address: {verification_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[form.cleaned_data['email']],
            )
            messages.success(request, 'Account created! Please check your email to verify your account.')
            return redirect('user:login')
    else:
        form = RegisterForm()
    return render(request, 'user/register.html', {'form': form})


def safe_decimal(val):
    try:
        return Decimal(val)
    except (TypeError, ValueError, InvalidOperation):
        return Decimal('0.00')


@login_required
def dashboard(request):
    try:
        kyc = request.user.kycsubmission
    except KYCSubmission.DoesNotExist:
        kyc = None

    profile = getattr(request.user, 'userprofile', None)
    recent_applications = LoanApplication.objects.filter(user=request.user).order_by('-submitted_at')[:5]
    deposits = DepositTransaction.objects.filter(user=request.user).order_by('-submitted_at')

    repayment_alert = False
    if profile and getattr(profile, "repayment_alert_pending", False):
        repayment_alert = True
        profile.repayment_alert_pending = False
        profile.save()

    print("DEBUG: repayment_alert in dashboard view:", repayment_alert)  # <-- Add here

    # Sanitize all decimals
    if profile:
        try:
            profile.balance = safe_decimal(getattr(profile, 'balance', 0))
        except Exception:
            profile.balance = Decimal('0.00')
        try:
            profile.active_loan = safe_decimal(getattr(profile, 'active_loan', 0))
        except Exception:
            profile.active_loan = Decimal('0.00')

    for app in recent_applications:
        try:
            app.loan_amount = safe_decimal(getattr(app, 'loan_amount', 0))
        except Exception:
            app.loan_amount = Decimal('0.00')

    for deposit in deposits:
        try:
            deposit.amount = safe_decimal(getattr(deposit, 'amount', 0))
        except Exception:
            deposit.amount = Decimal('0.00')

    profile = request.user.userprofile
    twofa_alert_permanently_dismissed = request.user.is_verified
    twofa_alert_temporarily_dismissed = (
        profile.twofa_alert_dismissed_until and profile.twofa_alert_dismissed_until > timezone.now()
    )
    # Add this check
    has_2fa = TOTPDevice.objects.filter(user=request.user, confirmed=True).exists()
    context = {
        'wallet_balance': profile.balance if profile else Decimal('0.00'),
        'active_loan': profile.active_loan if profile else Decimal('0.00'),
        'next_repayment': '2025-08-01',
        'crypto_coins': [
            {
                'name': 'Bitcoin',
                'symbol': 'btc',
                'icon_url': 'https://assets.coingecko.com/coins/images/1/small/bitcoin.png',
                'price': '67000',
                'change': '+2.5'
            },
            {
                'name': 'Ethereum',
                'symbol': 'eth',
                'icon_url': 'https://assets.coingecko.com/coins/images/279/small/ethereum.png',
                'price': '3500',
                'change': '-1.2'
            },
            {
                'name': 'Solana',
                'symbol': 'sol',
                'icon_url': 'https://assets.coingecko.com/coins/images/4128/small/solana.png',
                'price': '150',
                'change': '+0.8'
            }
        ],
        'transactions': [
            {
                'date': '2025-07-15',
                'description': 'Loan Repayment',
                'status': 'Completed',
                'status_class': 'success',
                'amount': '-$200.00'
            },
            {
                'date': '2025-07-10',
                'description': 'Deposit',
                'status': 'Completed',
                'status_class': 'success',
                'amount': '+$500.00'
            },
            {
                'date': '2025-07-05',
                'description': 'Withdrawal',
                'status': 'Pending',
                'status_class': 'warning',
                'amount': '-$100.00'
            }
        ],
        'kyc': kyc,
        'profile': profile,
        'recent_applications': recent_applications,
        'deposits': deposits,
        'repayment_alert': repayment_alert,
        "twofa_alert_permanently_dismissed": twofa_alert_permanently_dismissed,
        "twofa_alert_temporarily_dismissed": twofa_alert_temporarily_dismissed,
        'has_2fa': has_2fa,
    }

    return render(request, 'user/dashboard.html', context)


def withdraw(request):
    return render(request, 'user/withdraw.html')


def repay(request):
    return render(request, 'user/repay.html')


def transactions(request):
    deposits = DepositTransaction.objects.filter(user=request.user).order_by('-submitted_at')
    return render(request, 'user/transactions.html', {'deposits': deposits})


def help_center(request):
    return render(request, 'user/help.html')


def transactions(request):
    user_profile = UserProfile.objects.filter(user=request.user).first()
    deposits = DepositTransaction.objects.filter(user=request.user).order_by('-submitted_at')
    loans = LoanApplication.objects.filter(user=request.user).order_by('-submitted_at')
    return render(request, 'user/transactions.html', {
        'user_profile': user_profile,
        'deposits': deposits,
        'loans': loans,
    })


@login_required
def loan_apply(request):
    # Check if KYC is verified
    try:
        kyc = request.user.kycsubmission
        if kyc.current_step != 'submitted':
            messages.warning(request, "You must complete and submit your KYC before applying for a loan.")
            return redirect('user:dashboard')  # updated
    except KYCSubmission.DoesNotExist:
        messages.warning(request, "You must complete and submit your KYC before applying for a loan.")
        return redirect('user:dashboard')  # updated

    # Check for any loan application under review
    pending = LoanApplication.objects.filter(user=request.user, status='review').exists()
    if pending:
        messages.warning(request, "You already have a loan application under review. Please wait for it to be approved or rejected before applying again.")
        return redirect('user:dashboard')  # updated

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
    if request.method == 'POST':
        data = request.POST
        required_fields = [
            'first_name', 'last_name', 'dob', 'country', 'address', 'email', 'phone', 'taxpayer_id',
            'employment_status', 'employer', 'job_title', 'monthly_income', 'income_source',
            'loan_purpose', 'loan_amount', 'loan_currency', 'loan_term', 'repayment_plan',
            'collateral', 'collateral_amount', 'collateral_wallet', 'agree_terms', 'confirm_accuracy'
        ]
        missing = [field for field in required_fields if not data.get(field)]
        if missing:
            messages.error(request, f"Please fill in all fields: {', '.join(missing)}")
            return render(request, 'user/loan_apply.html', {'loan_types': loan_types})

        # Remove commas from decimal fields
        loan_amount = data.get('loan_amount', '').replace(',', '')
        collateral_amount = data.get('collateral_amount', '').replace(',', '')
        monthly_income = data.get('monthly_income', '').replace(',', '')
        LoanApplication.objects.create(
            user=request.user,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            dob=data.get('dob'),
            country=data.get('country'),
            address=data.get('address'),
            email=data.get('email'),
            phone=data.get('phone'),
            taxpayer_id=data.get('taxpayer_id'),
            employment_status=data.get('employment_status'),
            employer_name=data.get('employer'),
            job_title=data.get('job_title'),
            monthly_income=monthly_income,
            income_source=data.get('income_source'),
            loan_purpose=data.get('loan_purpose'),
            loan_amount=loan_amount,
            loan_currency=data.get('loan_currency'),
            loan_term=data.get('loan_term'),
            repayment_plan=data.get('repayment_plan'),
            existing_loan=bool(data.get('existing_loan')),
            collateral_type=data.get('collateral'),
            collateral_amount=collateral_amount,
            wallet_address=data.get('collateral_wallet'),
            agree_terms=bool(data.get('agree_terms')),
            confirm_info_accuracy=bool(data.get('confirm_accuracy')),
        )

        messages.success(request, "Your loan application has been submitted and is under review.")
        return redirect('user:dashboard')
    return render(request, 'user/loan_apply.html', {
        'loan_types': loan_types,
    })


def repay(request):
    return render(request, 'user/repay.html')


def withdraw(request):
    return render(request, 'user/withdraw.html')


def deposit(request):
    return render(request, 'user/deposit.html')


def kyc_verify(request):
    return render(request, 'user/kyc_verify.html')


@login_required
def profile_settings(request):
    user = request.user
    profile = user.userprofile
    if request.method == "POST":
        if 'change_email' in request.POST:
            new_email = request.POST.get('new_email')
            if new_email and new_email != user.email:
                # Generate token
                token = secrets.token_urlsafe(32)
                profile.pending_email = new_email
                profile.email_verification_token = token
                profile.save()
                # Send verification email
                verification_url = request.build_absolute_uri(
                    reverse('user:verify_email', args=[token])
                )
                send_mail(
                    subject="Verify your new email address",
                    message=f"Click the link to verify your new email address: {verification_url}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[new_email],
                )
                messages.info(request, "A verification link has been sent to your new email address.")
            return redirect('user:profile_settings')
        elif 'update_picture' in request.POST:
            picture = request.FILES.get('profile_picture')
            if picture:
                profile.profile_picture = picture
                profile.save()
            return redirect('user:profile_settings')
        else:
            form = SettingsForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('user:profile_settings')
    else:
        form = SettingsForm(instance=user)
    return render(request, 'user/settings.html', {
        'form': form,
        'login_activities': [],  # your logic here
    })


def help_page(request):
    return render(request, 'user/help.html')


def notifications(request):
    return render(request, 'user/notifications.html')


def user_logout(request):
    logout(request)
    return redirect('home')


@require_POST
@login_required
def dismiss_kyc_verified_alert(request):
    kyc = request.user.kycsubmission
    kyc.kyc_verified_alert_dismissed = True
    kyc.save()
    return JsonResponse({'success': True})


def deposit_success(request):
    return render(request, 'user/deposit-success.html')



def settings_profile(request):
    return render(request, 'user/settings_profile.html')


@login_required
def profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _("Profile updated successfully."))
            return redirect('user:profile')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    return render(request, 'user/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


# @login_required
# def deposit_history(request):
#     deposits = DepositTransaction.objects.filter(user=request.user).order_by('-submitted_at')
#     return render(request, 'user/deposit_history.html', {'deposits': deposits})

def verify_email(request, token):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    profile = UserProfile.objects.filter(email_verification_token=token).first()
    if profile and profile.user and not profile.user.is_active:
        profile.user.is_active = True
        profile.user.email = profile.pending_email or profile.user.email  # Use pending_email if set
        profile.user.save()
        profile.pending_email = None
        profile.email_verification_token = None
        profile.save()
        messages.success(request, "Your account has been verified. You can now log in.")
        return redirect('user:login')
    elif profile and profile.pending_email:
        # This is for email change, as before
        profile.user.email = profile.pending_email
        profile.user.save()
        profile.pending_email = None
        profile.email_verification_token = None
        profile.save()
        messages.success(request, "Your email address has been updated and verified.")
        return redirect('user:profile_settings')
    else:
        messages.error(request, "Invalid or expired verification link.")
        return redirect('user:login')


from django.shortcuts import render

def test_disable(request):
    return render(request, 'two_factor/core/disable.html')


class CustomDisable2FAView(DisableView):
    def dispatch(self, request, *args, **kwargs):
        # If user is a social user (no password), handle disable here for both GET and POST
        if not request.user.has_usable_password():
            if request.method == 'POST':
                from django_otp.plugins.otp_totp.models import TOTPDevice
                TOTPDevice.objects.filter(user=request.user).delete()
                messages.success(request, "Two-Factor Authentication has been disabled.")
                return redirect('user:profile_settings')
            # For GET, just show a confirmation page or redirect to settings
            return redirect('user:profile_settings')
        # Otherwise, use the default behavior
        return super().dispatch(request, *args, **kwargs)


@login_required
def dismiss_twofa_alert(request):
    if request.method == "POST":
        profile = request.user.userprofile
        profile.twofa_alert_dismissed_until = timezone.now() + timedelta(minutes=30)
        profile.save()
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)


def post_signup(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('user:login')

    profile = getattr(user, 'userprofile', None)
    # If already set, skip
    if profile and profile.country and profile.currency:
        return redirect('user:dashboard')

    # Show form and handle POST
    if request.method == 'POST':
        country = request.POST.get('country')
        currency = request.POST.get('currency')
        if country and currency:
            if not profile:
                from .models import UserProfile
                profile = UserProfile.objects.create(user=user)
            profile.country = country
            profile.currency = currency
            profile.save()
            return redirect('user:dashboard')
        else:
            messages.error(request, 'Please select both country and currency.')

    # Prepare choices for template
    from .models import UserProfile
    country_choices = [
        ('US', 'United States'),
        ('GB', 'United Kingdom'),
        ('NG', 'Nigeria'),
        ('CA', 'Canada'),
        ('IN', 'India'),
        # ... add more as needed ...
    ]
    currency_choices = UserProfile.CURRENCY_CHOICES
    return render(request, 'user/post_signup.html', {
        'country_choices': country_choices,
        'currency_choices': currency_choices,
    })


class CustomSetup2FAView(SetupView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('user:login')
        # Do NOT block users without password!
        return super().dispatch(request, *args, **kwargs)


class CustomTwoFactorLoginView(LoginView):
    form_list = (
        ('auth', CustomAuthenticationTokenForm),
        ('token', AuthenticationTokenForm),
        ('backup', BackupTokenForm),
    )

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        if step == 'auth':
            kwargs['request'] = self.request
            # For social users, don't require password
            if self.request.user.is_authenticated and not self.request.user.has_usable_password():
                kwargs['password_required'] = False
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        # If user is authenticated via social login and has 2FA, skip auth step
        if (
            request.user.is_authenticated and
            self.has_device() and
            hasattr(request.user, 'socialaccount_set') and
            request.user.socialaccount_set.exists()
        ):
            return self.render_next_step(self.get_next_step('auth'))
        return super().dispatch(request, *args, **kwargs)

    def has_device(self):
        user = self.request.user
        return (
            user.is_authenticated and
            TOTPDevice.objects.filter(user=user, confirmed=True).exists()
        )