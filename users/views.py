from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, InvestmentForm
from .models import Profile, Investment
from .utils import get_stock_price

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        auth_logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect('login')
    return render(request, 'users/logout.html')

@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    investments = Investment.objects.filter(user=request.user)
    investments_with_values = []
    for investment in investments:
        current_value = investment.current_value()  #Calculate current value
        profit_or_loss = investment.profit_or_loss()  #Calculate profit or loss
        investments_with_values.append({
            'investment': investment,
            'current_value': current_value,
            'profit_or_loss': profit_or_loss
        })
    return render(request, 'users/profile.html', {
        'profile': profile,
        'investments_with_values': investments_with_values
    })

#API from AlphaVantage
api_key = "OWSXIPKVLK7APWRW"

@login_required
def invest_view(request):
    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment = form.save(commit=False)
            investment.user = request.user
            investment.shares = investment.amount_invested / get_stock_price(investment.stock_symbol)
            profile = Profile.objects.get(user=request.user)
            if profile.coins >= investment.amount_invested:
                investment.save()
                profile.coins -= investment.amount_invested
                profile.save()
                return redirect('profile')
            else:
                messages.error(request, "Not enough coins to invest.")
    else:
        form = InvestmentForm()
    return render(request, 'users/invest.html', {'form': form})
