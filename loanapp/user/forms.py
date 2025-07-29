from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from .models import KYCSubmission, UserProfile, DepositTransaction  # <-- Add UserProfile import
from django_countries.widgets import CountrySelectWidget
from adminpanel.models import DepositMethod, CryptoWallet, BankAccount
from two_factor.forms import AuthenticationTokenForm, BackupTokenForm

ADDRESS_DOC_TYPE_CHOICES = [
    ('Utility Bill', 'Utility Bill'),
    ('Bank Statement', 'Bank Statement'),
    ('Tenancy Agreement', 'Tenancy Agreement'),
    ('Tax Bill', 'Tax Bill'),
]

ID_TYPE_CHOICES = [
    ('National ID', 'National ID'),
    ("Driver's License", "Driver's License"),
    ('International Passport', 'International Passport'),
    ("Voter's Card", "Voter's Card"),
]


# 1. Form for step 1: selecting method and entering amount
class DepositInitiateForm(forms.Form):
    method = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_method'})
    )
    coin = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_coin'})
    )
    amount = forms.DecimalField(
        label="Amount (USD)",
        min_value=1,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        deposit_methods = kwargs.pop('deposit_methods', [])
        crypto_options = kwargs.pop('crypto_options', [])
        super().__init__(*args, **kwargs)
        self.fields['method'].choices = [(m.slug, m.name) for m in deposit_methods]
        self.fields['coin'].choices = [(c.pk, c.coin) for c in crypto_options]


# 2. Form for step 2: uploading payment proof
class DepositProofForm(forms.ModelForm):
    class Meta:
        model = DepositTransaction
        fields = ['proof']
        widgets = {
            'proof': forms.FileInput(attrs={'class': 'form-control', 'required': True})
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username or email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(username=username_or_email, password=password)

        # Try email login fallback if username fails
        if user is None:
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(username=user_obj.username, password=password)
                if user is None:
                    raise forms.ValidationError("Invalid login credentials.")
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid login credentials.")

        self.user_cache = user
        return cleaned_data


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Your Email'
        })
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Your Username'
        })
    )

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password'
        })
    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
    )

    currency = forms.ChoiceField(
        choices=UserProfile.CURRENCY_CHOICES,
        label="Preferred Currency",
        widget=forms.Select(attrs={'class': 'form-select'})  # <-- Add this line
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class KYCAddressForm(forms.ModelForm):
    address_doc_type = forms.ChoiceField(
        choices=ADDRESS_DOC_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = KYCSubmission
        fields = [
            'full_name',
            'street_address',
            'city',
            'state',
            'postal_code',
            'country',
            'address_doc_type',
            'address_proof'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. John Doe'
            }),
            'street_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 123 Main St'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. New York'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. NY'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 10001'
            }),
            'country': CountrySelectWidget(attrs={'class': 'form-select'}),
            'address_proof': forms.FileInput(attrs={'class': 'form-control'}),
        }


class KYCIdentityForm(forms.ModelForm):
    id_type = forms.ChoiceField(
        choices=ID_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = KYCSubmission
        fields = [
            'id_type',
            'id_number',
            'id_document',
        ]
        widgets = {
            'id_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. A123456789'
            }),
            'id_document': forms.FileInput(attrs={'class': 'form-control'}),
        }


class DepositForm(forms.Form):
    method = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_method'})
    )
    coin = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_coin'})
    )
    amount = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['currency']  # Add other UserProfile fields you want editable


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class SettingsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['language', 'currency', 'timezone']
        widgets = {
            'language': forms.Select(
                attrs={'class': 'form-select'},
                choices=[
                    ('English (United States)', 'English (United States)'),
                    ('Spanish', 'Spanish'),
                    ('French', 'French'),
                    ('Chinese', 'Chinese'),
                ]
            ),
            'currency': forms.Select(
                attrs={'class': 'form-select'},
                choices=UserProfile.CURRENCY_CHOICES
            ),
            'timezone': forms.Select(
                attrs={'class': 'form-select'},
                choices=[
                    ('(GMT-12:00) International Date Line West', '(GMT-12:00) International Date Line West'),
                    ('(GMT-06:00) Central America', '(GMT-06:00) Central America'),
                    ('(GMT+01:00) West Africa Time', '(GMT+01:00) West Africa Time'),
                ]
            ),
        }


class CustomAuthenticationTokenForm(AuthenticationTokenForm):
    def __init__(self, *args, request=None, password_required=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        # Remove password field for social users
        if self.request and self.request.user.is_authenticated and not self.request.user.has_usable_password():
            if 'password' in self.fields:
                self.fields['password'].required = False
                self.fields['password'].widget.attrs['disabled'] = True
                self.fields['password'].widget.attrs['placeholder'] = 'Not required for social login'