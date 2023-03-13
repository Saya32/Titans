# Create your views here.
import json
from django.shortcuts import render, redirect
from .models import User, Transaction, Category, Chart
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Transaction, Category
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from .forms import SignUpForm, LogInForm, CategoryDetailsForm, ChangePasswordForm, UserForm, TransactionForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.views import View
from django.views.generic.edit import FormView
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import  UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .helpers import get_user_transactions, get_categories, get_user_balance, get_user_income, get_user_expense, get_user_budget, change_transaction_name, delete_transactions
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import BytesIO
from spendingtrackers.models import Transaction
import datetime 
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from django.db.models import Sum
from django.http import JsonResponse
from datetime import datetime

from datetime import datetime



class LoginProhibitedMixin:
    """Mixin that redirects when a user is logged in."""

    redirect_when_logged_in_url = None

    def dispatch(self, *args, **kwargs):
        """Redirect when logged in, or dispatch as normal otherwise."""
        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        return super().dispatch(*args, **kwargs)

    def handle_already_logged_in(self, *args, **kwargs):
        url = self.get_redirect_when_logged_in_url()
        return redirect(url)

    def get_redirect_when_logged_in_url(self):
        """Returns the url to redirect to when not logged in."""
        if self.redirect_when_logged_in_url is None:
            raise ImproperlyConfigured(
                "LoginProhibitedMixin requires either a value for "
                "'redirect_when_logged_in_url', or an implementation for "
                "'get_redirect_when_logged_in_url()'."
            )
        else:
            return self.redirect_when_logged_in_url


class LogInView(LoginProhibitedMixin, View):
    """View that handles log in."""

    http_method_names = ['get', 'post']
    redirect_when_logged_in_url = 'feed'

    def get(self, request):
        """Display log in template."""

        self.next = request.GET.get('next') or ''
        return self.render()

    def post(self, request):
        """Handle log in attempt."""

        form = LogInForm(request.POST)
        self.next = request.POST.get('next') or settings.REDIRECT_URL_WHEN_LOGGED_IN
        user = form.get_user()
        if user is not None:
            login(request, user)
            return redirect(self.next)

        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
        return self.render()

    def render(self):
        """Render log in template with blank log in form."""

        form = LogInForm()
        return render(self.request, 'log_in.html', {'form': form, 'next': self.next})


class SignUpView(LoginProhibitedMixin, FormView):
    """View that signs up user."""

    form_class = SignUpForm
    template_name = "sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


def home_page(request):
    return render(request, 'home_page.html')


def feed(request):
    return render(request, 'feed.html')


def log_out(request):
    logout(request)
    return redirect('home_page')

class ProfileUpdateView(LoginRequiredMixin, UpdateView):

    """View to update logged-in user's profile."""
    model = UserForm
    template_name = "profile.html"
    form_class = UserForm



    def get_object(self):
        """Return the object (user) to be updated."""
        user = self.request.user
        return user


    def get_success_url(self):
        """Return redirect URL after successful update."""
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)

def new_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            category_name=form.cleaned_data['category']
            category_object = get_object_or_404(Category, user = request.user, name=category_name)
            
            Transaction.objects.create(
                user=request.user,
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                amount=form.cleaned_data.get('amount'),
                date_paid=form.cleaned_data.get('date_paid'),
                time_paid=form.cleaned_data.get('time_paid'),
                category=form.cleaned_data.get('category'),
                receipt=form.cleaned_data.get('receipt'),
                transaction_type=form.cleaned_data.get('transaction_type'),
                category_fk= category_object
            )
            return redirect('feed')
        else:
            return render(request, 'new_transaction.html', {'form': form})
    else:
        form = TransactionForm()
        return render(request, 'new_transaction.html', {'form': form})


def records(request):
    transactions = get_user_transactions(request.user)
    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        if from_date and to_date:
            from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
            transactions = transactions.filter(date_paid__range=[from_date_obj, to_date_obj])
    return render(request, 'records.html', {'transactions': transactions})
    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        if from_date and to_date:
            from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
            transactions = transactions.filter(date_paid__range=[from_date_obj, to_date_obj])
    return render(request, 'records.html', {'transactions': transactions})


def chart_balance_graph(request):
    # Retrieve user's transactions
    transactions = Transaction.objects.filter(user=request.user).order_by('date_paid')
    
    # Extract data for graph
    labels = []
    data = []
    balance = 0
    for transaction in transactions:
        labels.append(transaction.date_paid.strftime("%m/%d/%Y"))
        if transaction.transaction_type == "Expense":
            balance -= transaction.amount
        else:
            balance += transaction.amount
        data.append(balance)
    
    # Create chart data
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
    
def chart_expense_graph(request):
    # Retrieve user's transactions
    transactions = Transaction.objects.filter(user=request.user).order_by('date_paid')
    # Extract data for graph
    labels = []
    data = []
    expense = 0
    for transaction in transactions:
        labels.append(transaction.date_paid.strftime("%m/%d/%Y"))
        if transaction.transaction_type == "Expense":
            expense = transaction.amount
        else:
            expense != transaction.amount
        data.append(expense)
    # Create chart data
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def expense_pie_chart(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('category')
    labels = []
    data = []
    expenses = 0
    for transaction in transactions:
        labels.append(transaction.category)
        if transaction.transaction_type == "Expense":
            expenses = transaction.amount
        data.append(expenses)

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


    

def update_record(request, id):
    try:
        record = Transaction.objects.get(pk=id)
    except:
        messages.add_message(request, messages.ERROR, "Record could not be found!")
        return redirect('feed')

    if request.method == 'POST':
        form = TransactionForm(instance = record, data = request.POST)
        if (form.is_valid()):
            messages.add_message(request, messages.SUCCESS, "Record updated!")
            form.save()
            return redirect('feed')
        else:
            return render(request, 'update_record.html', {'form': form, 'transaction' : record})
    else:
        form = TransactionForm(instance = record)
        return render(request, 'update_record.html', {'form': form, 'transaction' : record})

def delete_record(request, id):
    if (Transaction.objects.filter(pk=id)):
        Transaction.objects.filter(pk=id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted!")
        return redirect('feed')
    else:
        messages.add_message(request, messages.ERROR, "Sorry, an error occurred deleting your record.")
        return redirect('feed')


def change_password(request):
    if request.method == 'POST':
        userform = ChangePasswordForm(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            his_password = userform.cleaned_data['his_password']
            password = userform.cleaned_data['password']
            password_confirmation = userform.cleaned_data['password_confirmation']
            if password != password_confirmation:
                messages.add_message(request, messages.ERROR, "The two passwords are inconsistent!")
                return render(request, 'change_password.html')
            user = User.objects.filter(username__exact=username).first()
            if not user:
                messages.add_message(request, messages.ERROR, "email not exists!")
                return render(request, 'change_password.html')
            if not check_password(his_password, user.password):
                messages.add_message(request, messages.ERROR, "history password error!")
                return render(request, 'change_password.html')
            user.password = make_password(password)
            user.save()
            return render(request, 'log_in.html')
        else:
            return render(request, 'change_password.html')
    else:
        return render(request, 'change_password.html')



def edit_category_details(request, id):
    try:
        category = Category.objects.get(pk=id, user=request.user)
    except:
        messages.add_message(request, messages.ERROR, "Category could not be found!")
        return redirect('category')

    if request.method == 'POST':
        form = CategoryDetailsForm(instance = category, data = request.POST)
        if (form.is_valid()):
            change_transaction_name(request.user, category)
            messages.add_message(request, messages.SUCCESS, "Category updated!")
            form.save()
            return redirect('category')
        else:
            return render(request, 'edit_category_details.html', {'form': form, 'category' : category})
    else:
        form = CategoryDetailsForm(instance = category)
        return render(request, 'edit_category_details.html', {'form': form, 'category' : category})

def delete_category(request, id):
    if (Category.objects.filter(pk=id)):
        category = Category.objects.filter(pk=id)
        delete_transactions(request.user, category)
        Category.objects.filter(pk=id).delete()
        messages.add_message(request, messages.SUCCESS, "Category deleted!")
        return redirect('feed')
    else:
        messages.add_message(request, messages.ERROR, "Sorry, an error occurred deleting your Category")
        return redirect('feed')



def category(request):
   categories = get_categories(request.user.id)
   return render(request, 'category.html', {'categories':categories})

def view_category(request, id):
    try:
        category = Category.objects.get(pk=id)
    except:
        messages.add_message(request, messages.ERROR, "Category could not be found!")
        return redirect('feed')

    transactions = get_user_transactions(request.user)
    expense = category.get_expenses()
    income = category.get_income()
    balance = category.get_balance()
   
    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        if from_date and to_date:
            from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
            transactions = transactions.filter(date_paid__range=[from_date_obj, to_date_obj])
            expense = category.get_expenses(from_date=from_date_obj, to_date=to_date_obj)
            income = category.get_income(from_date=from_date_obj, to_date=to_date_obj)
            balance = category.get_balance(from_date=from_date_obj, to_date=to_date_obj)
    
    if category.budget is not None:
        used_percentage = expense / category.budget * 100
        used_percentage = round(used_percentage, 2)
    else:
        used_percentage = None
    
    if balance < 0:
        warning_message = "Warning: You have exceeded your budget for this category."
    elif used_percentage is not None and used_percentage >= 90:
        warning_message = "Warning: You have used {}% of your budget for this category.".format(used_percentage)
    else:
        warning_message = None

    context = {'category': category, 'transactions': transactions, 'expense': expense, 'income': income, 'balance': balance, 'warning_message': warning_message}
    return render(request, 'view_category.html', context)

def dashboard(request):
    balance_data = chart_balance_graph(request)
    expense_data = chart_expense_graph(request)
    expense_structure = expense_pie_chart(request)
    context = {
        'balance_data': balance_data,
        'expense_data': expense_data,
        'expense_pie_chart': expense_structure,
        # other context variables
    }
    return render(request, 'dashboard.html')

def add_category_details(request):
    if request.method == 'POST':
        form = CategoryDetailsForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, "Category added.")
            return redirect('category')
        else:
            messages.error(request, "Invalid form data.")
    else:
        form = CategoryDetailsForm()

    return render(request, 'add_category_details.html', {'form': form})

def overall(request):
    transactions = get_user_transactions(request.user)
    expense = get_user_expense(request.user)
    income = get_user_income(request.user)
    balance = get_user_balance(request.user)
    budget = get_user_budget(request.user)
    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        if from_date and to_date:
            from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
            transactions = transactions.filter(date_paid__range=[from_date_obj, to_date_obj])
            expense = get_user_expense(request.user,from_date=from_date_obj, to_date=to_date_obj)
            income = get_user_income(request.user,from_date=from_date_obj, to_date=to_date_obj)
            balance = get_user_balance(request.user,from_date=from_date_obj, to_date=to_date_obj)
            budget = get_user_budget(request.user,from_date=from_date_obj, to_date=to_date_obj)
    
    if budget:
        used_percentage = expense / budget * 100
        used_percentage = round(used_percentage, 2)
    else:
        used_percentage = None
    
    if balance < 0:
        warning_message = "Warning: You have exceeded your budget for this category."
    elif used_percentage is not None and used_percentage >= 90:
        warning_message = "Warning: You have used {}% of your budget for this category.".format(used_percentage)
    else:
        warning_message = None

    context = {'category': category, 'transactions': transactions, 'expense': expense, 'income': income, 'balance': balance, 'budget':budget,'warning_message': warning_message,}
    return render(request, 'overall.html', context)
