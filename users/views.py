from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .models import Profile

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
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
                login(request, user)
                return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        auth_logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect('login')  # Redirect to the login page after logout
    return render(request, 'users/logout.html')

#User profile

# @login_required
# def profile_view(request):
#     return render(request, 'users/profile.html')

@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    investments = profile.investments
    return render(request, 'users/profile.html', {'profile': profile, 'investments': investments})

#Investment feature

# @login_required
# def invest_view(request):
#     if request.method == 'POST':
#         stock_name = request.POST.get('stock_name')
#         amount = int(request.POST.get('amount'))
#         profile = Profile.objects.get(user=request.user)
#         if profile.coins >= amount:
#             profile.coins -= amount
#             if stock_name in profile.investments:
#                 profile.investments[stock_name] += amount
#             else:
#                 profile.investments[stock_name] = amount
#             profile.save()
#             messages.success(request, 'Investment successful!')
#         else:
#             messages.error(request, 'Insufficient coins!')
#         return redirect('profile')
#     return render(request, 'users/invest.html')

@login_required
def invest_view(request):
    if request.method == 'POST':
        # Handle the investment logic here
        stock = request.POST.get('stock_name')
        amount = int(request.POST.get('amount'))
        
        profile = Profile.objects.get(user=request.user)
        if profile.coins >= amount:
            profile.coins -= amount
            profile.investments[stock] = profile.investments.get(stock, 0) + amount
            profile.save()
            return redirect('profile')
        else:
            messages.error(request, "Not enough coins to invest.")

    return render(request, 'users/invest.html')
