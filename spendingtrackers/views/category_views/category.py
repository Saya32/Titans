# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from ..models import User, Transaction, Category, Achievement, Chart
from django.contrib.auth.decorators import login_required
from django.shortcuts import render



@login_required
def category(request):
    categories = get_categories(request.user.id)
    return render(request, 'category.html', {'categories': categories})

