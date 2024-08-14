from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Investment

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ['stock_symbol', 'amount_invested']

    def clean(self):
        cleaned_data = super().clean()
        amount_invested = cleaned_data.get("amount_invested")
        return cleaned_data