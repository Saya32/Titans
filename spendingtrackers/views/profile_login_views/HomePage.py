# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def home_page(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'feed.html')
    return render(request, 'home_page.html')


@login_required
def sign_success(request):
    return render(request, 'sign_success.html')


@login_required
def banner(request):
    return render(request, 'banner.html')


@login_required
def feed(request):
    return render(request, 'feed.html')


@login_required
def log_out(request):
    logout(request)
    return redirect('home_page')
