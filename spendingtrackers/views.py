# Create your views here.
import re
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Transaction, Category
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import SignUpForm, LogInForm, CategoryDetailsForm, UserForm, TransactionForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.views import View
from django.views.generic.edit import FormView
from django.urls import reverse
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from .helpers import get_user_transactions, get_categories, get_user_balance, get_user_income, get_user_expense, get_user_budget, change_transaction_name, delete_transactions, set_achievements, get_achievements, update_achievements
from django.contrib.auth.hashers import make_password
import matplotlib.pyplot as plt
from spendingtrackers.models import Transaction
from django.shortcuts import render
from django.http import JsonResponse
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


def forgot_password(request):
    if request.method == 'POST':
        user_name = request.POST['email']
        pin = request.POST['pin']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']
        regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$'
        if not re.match(regex, password):
            messages.add_message(request, messages.ERROR, 'Password must contain an uppercase character, a lowercase '
                                                          'character and a number')
            return render(request, 'forgot_password.html')
        user = User.objects.filter(username__exact=user_name).first()
        if not user:
            messages.add_message(request, messages.ERROR, "email does not exist!")
            return render(request, 'forgot_password.html')
        if user.pin != pin:
            messages.add_message(request, messages.ERROR, "pin error!")
            return render(request, 'forgot_password.html')
        if password != password_confirmation:
            messages.add_message(request, messages.ERROR, "The two passwords are inconsistent!")
            return render(request, 'forgot_password.html')
        user.password = make_password(password)
        user.save()
        messages.add_message(request, messages.SUCCESS, "SUCCESS!")
        return render(request, 'forgot_password.html')
    else:
        return render(request, 'forgot_password.html')


class SignUpView(LoginProhibitedMixin, FormView):
    """View that signs up user."""

    form_class = SignUpForm
    template_name = "sign_up.html"
    redirect_when_logged_in_url = 'sign_success'

    def form_valid(self, form):
        self.object = form.save()
        set_achievements(self.object)
        update_achievements(self.object)
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(self.redirect_when_logged_in_url)


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


@login_required
def new_transaction(request):
    try:
        if request.method == 'POST':
            form = TransactionForm(request.POST, request.FILES)
            if form.is_valid():
                category_name = form.cleaned_data['category']
                category_object = get_object_or_404(Category, user=request.user, name=category_name)

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
                    category_fk=category_object
                )
                update_achievements(request.user)
                return redirect('feed')
            else:
                return render(request, 'new_transaction.html', {'form': form})
        else:
            form = TransactionForm()
            return render(request, 'new_transaction.html', {'form': form})
    except:
        messages.add_message(request, messages.ERROR, "Error: Category does not exist")
        return redirect('category')



@login_required
def records(request):
    transactions = get_user_transactions(request.user)
    currency = request.user.currency
    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        if from_date and to_date:
            from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
            transactions = transactions.filter(date_paid__range=[from_date_obj, to_date_obj])
    return render(request, 'records.html', {'transactions': transactions,'currency': currency})


def chart_balance_graph(request):
    # Retrieve user's transactions
    transactions = Transaction.objects.filter(user=request.user).order_by('date_paid')
    if request.method == 'GET':
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        if from_date and to_date:
            from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
            transactions = transactions.filter(date_paid__range=[from_date_obj, to_date_obj])
    
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
        data.append(int(balance))
    
    # Create chart data
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
    
def chart_expense_graph(request):
    # Retrieve user's transactions
    transactions = Transaction.objects.filter(user=request.user).order_by('date_paid')
    if request.method == 'GET':
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        if from_date and to_date:
            from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
            transactions = transactions.filter(date_paid__range=[from_date_obj, to_date_obj])
    # Extract data for graph
    labels = []
    data = []
    expense = 0
    for transaction in transactions:
        labels.append(transaction.date_paid.strftime("%m/%d/%Y"))

        if transaction.transaction_type == "Expense":
            expense = transaction.amount
        else:
            expense = 0
        data.append(float(expense))
    # Create chart data
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def chart_income_graph(request):
    # Retrieve user's transactions
    transactions = Transaction.objects.filter(user=request.user).order_by('date_paid')
    if request.method == 'GET':
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        if from_date and to_date:
            from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
            transactions = transactions.filter(date_paid__range=[from_date_obj, to_date_obj])
    # Extract data for graph
    labels = []
    data = []
    income = 0
    for transaction in transactions:
        labels.append(transaction.date_paid.strftime("%m/%d/%Y"))
        if transaction.transaction_type == "Income":
            income = transaction.amount
        else:
            income = 0
        data.append(float(income))
    # Create chart data
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def expense_structure(request):
    # Retrieve user's transactions
    transactions = Transaction.objects.filter(user=request.user).order_by('category')
    if request.method == 'GET':
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        if from_date and to_date:
            from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
            transactions = transactions.filter(date_paid__range=[from_date_obj, to_date_obj])
    # Extract data for graph
    labels = []
    percentlabel = []
    data = {}
    total = 0
    expense = 0
    for transaction in transactions:
        if transaction.transaction_type == "Expense":
            total += transaction.amount
    for transaction in transactions:
        labels.append(transaction.category)
        if transaction.transaction_type == "Expense":
            expense = transaction.amount
        else:
            expense = 0
        if transaction.category in data:
            data[transaction.category] = round(int(data[transaction.category]) + expense)
        else:
            data[transaction.category] = expense
    # Create chart data
    return JsonResponse(data={
        'labels': labels,
        'total' : total,
        'percentlabel': percentlabel,
        'data': data,
    })

def expense_structure2(request):
    # Retrieve user's transactions
    transactions = Transaction.objects.filter(user=request.user).order_by('category')
    if request.method == 'GET':
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        if from_date and to_date:
            from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
            transactions = transactions.filter(date_paid__range=[from_date_obj, to_date_obj])
    # Extract data for graph
    labels = []
    data = {}
    expense = 0
    for transaction in transactions:
        labels.append(transaction.category)
        if transaction.transaction_type == "Expense":
            expense = transaction.amount
        else:
            expense = 0
        if transaction.category in data:
            data[transaction.category] = int(data[transaction.category]) + expense
        else:
            data[transaction.category] = expense
    # Create chart data
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


    

@login_required
def update_record(request, id):
    try:
        record = Transaction.objects.get(pk=id)
    except:
        messages.add_message(request, messages.ERROR, "Record could not be found!")
        return redirect('feed')

    
    if request.method == 'POST':
        form = TransactionForm(instance=record, data=request.POST)
        if (form.is_valid()):
            
            try:
                category_name = form.cleaned_data['category']
                category_object = get_object_or_404(Category, user=request.user, name=category_name)
            except:
                messages.add_message(request, messages.ERROR, "Category could not be found!")
                return redirect('feed')
            
            messages.add_message(request, messages.SUCCESS, "Record updated!")
            form.save()
            record = Transaction.objects.get(pk=id)
            record.category_fk = category_object
            record.save()
            return redirect('feed')
        else:
            return render(request, 'update_record.html', {'form': form, 'transaction': record})
    else:
        form = TransactionForm(instance=record)
        return render(request, 'update_record.html', {'form': form, 'transaction': record})


@login_required
def delete_record(request, id):
    if (Transaction.objects.filter(pk=id)):
        Transaction.objects.filter(pk=id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted!")
        return redirect('feed')
    else:
        messages.add_message(request, messages.ERROR, "Sorry, an error occurred deleting your record.")
        return redirect('feed')



@login_required
def edit_category_details(request, id):
    try:
        category = Category.objects.get(pk=id, user=request.user)
    except:
        messages.add_message(request, messages.ERROR, "Category could not be found!")
        return redirect('category')

    if request.method == 'POST':
        form = CategoryDetailsForm(instance=category, data=request.POST)
        if (form.is_valid()):
            change_transaction_name(request.user, category)
            messages.add_message(request, messages.SUCCESS, "Category updated!")
            form.save()
            return redirect('category')
        else:
            return render(request, 'edit_category_details.html', {'form': form, 'category': category})
    else:
        form = CategoryDetailsForm(instance=category)
        return render(request, 'edit_category_details.html', {'form': form, 'category': category})


@login_required
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


@login_required
def category(request):
    categories = get_categories(request.user.id)
    return render(request, 'category.html', {'categories': categories})


@login_required
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
    currency = request.user.currency

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

    if category.budget != 0 or None:
        used_percentage = (category.budget - balance) / category.budget * 100
        used_percentage = round(used_percentage, 2)
    else:
        used_percentage = None
    if balance < 0:
        warning_message = "Warning: You have exceeded your budget for this category."
    elif used_percentage is not None and used_percentage >= 90:
        warning_message = "Warning: You have used {}% of your budget for this category.".format(used_percentage)
    else:
        warning_message = None

    context = {'category': category, 'transactions': transactions, 'expense': expense, 'income': income,'balance': balance, 'warning_message': warning_message, 'currency':currency}
    return render(request, 'view_category.html', context)

@login_required
def dashboard(request):
    balance_data = chart_balance_graph(request)
    expense_data = chart_expense_graph(request)
    income_data = chart_income_graph(request)
    expense_structure_data = expense_structure(request)
    expense_structure_data2 = expense_structure2(request)
    
    context = {
        'balance_data': balance_data,
        'expense_data': expense_data,
        'income_data': income_data,
        'expense_structure_data': expense_structure_data,
        'expense_structure_data2': expense_structure_data2,
        # other context variables
    }
    return render(request, 'dashboard.html')


@transaction.atomic        #https://docs.djangoproject.com/en/4.1/topics/db/transactions/
@login_required
def add_category_details(request):
    try:
        if request.method == 'POST':
            form = CategoryDetailsForm(request.POST)
            if form.is_valid():
                category = form.save(commit=False)
                category.user = request.user
                category.save()
                update_achievements(request.user)
                messages.success(request, "Category added.")
                return redirect('category')
            else:
                messages.error(request, "Invalid form data.")
        else:
            form = CategoryDetailsForm()
        return render(request, 'add_category_details.html', {'form': form})
    except:
        with transaction.atomic(): #https://stackoverflow.com/questions/21458387/transactionmanagementerror-you-cant-execute-queries-until-the-end-of-the-atom
            messages.add_message(request, messages.ERROR, "Error: Category exists")
            return redirect('category')


@login_required
def overall(request):
    transactions = get_user_transactions(request.user)
    expense = get_user_expense(request.user)
    income = get_user_income(request.user)
    balance = get_user_balance(request.user)
    budget = get_user_budget(request.user)
    currency = request.user.currency
    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        if from_date and to_date:
            from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
            transactions = transactions.filter(date_paid__range=[from_date_obj, to_date_obj])
            expense = get_user_expense(request.user, from_date=from_date_obj, to_date=to_date_obj)
            income = get_user_income(request.user, from_date=from_date_obj, to_date=to_date_obj)
            balance = get_user_balance(request.user, from_date=from_date_obj, to_date=to_date_obj)
            budget = get_user_budget(request.user, from_date=from_date_obj, to_date=to_date_obj)

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

    context = {'category': category, 'transactions': transactions, 'expense': expense, 'income': income, 'balance': balance, 'budget':budget,'warning_message': warning_message,'currency':currency}
    return render(request, 'overall.html', context)


@login_required
def view_achievements(request):
   achievements = get_achievements(request.user.id)
   return render(request, 'view_achievements.html', {'achievements':achievements})