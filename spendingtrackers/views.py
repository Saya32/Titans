# Create your views here.
import json
from django.shortcuts import render, redirect
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
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .helpers import get_user_transactions, get_categories
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil import rrule


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


def sign_success(request):
    if not request.session.get('is_login'):
        return render(request, 'log_in.html')
    return render(request, 'sign_success.html')


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


def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'transaction_list.html', {'transactions': transactions})


def new_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            # update balance
            his_balance = request.user.balance
            if form.cleaned_data.get('transaction_type') == "Expense":
                if request.user.balance < form.cleaned_data.get('amount'):
                    messages.add_message(request, messages.ERROR, "Account balance Insufficient!")
                    return render(request, 'new_transaction.html', {'form': form})
                his_balance -= form.cleaned_data.get('amount')
            else:
                his_balance += form.cleaned_data.get('amount')

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
                # category_fk= request.user.get_category(form.cleaned_data.get('category'))
            )
            request.user.balance = his_balance
            request.user.save()
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


def update_record(request, id):
    try:
        record = Transaction.objects.get(pk=id)
        his_amount=record.amount
    except:
        messages.add_message(request, messages.ERROR, "Record could not be found!")
        return redirect('feed')

    if request.method == 'POST':
        form = TransactionForm(instance=record, data=request.POST)
        if (form.is_valid()):
            # add balance
            his_balance = request.user.balance
            if form.cleaned_data.get('transaction_type') == "Expense":
                if request.user.balance < form.cleaned_data.get('amount'):
                    messages.add_message(request, messages.ERROR, "Account balance Insufficient!")
                    return render(request, 'update_record.html', {'form': form})

                his_balance += his_amount
                his_balance -= form.cleaned_data.get('amount')
            else:
                his_balance -= his_amount
                his_balance += form.cleaned_data.get('amount')
            messages.add_message(request, messages.SUCCESS, "Record updated!")
            request.user.balance = his_balance
            request.user.save()
            form.save()
            return redirect('feed')
        else:
            return render(request, 'update_record.html', {'form': form, 'transaction': record})
    else:
        form = TransactionForm(instance=record)
        return render(request, 'update_record.html', {'form': form, 'transaction': record})


def delete_record(request, id):
    if (Transaction.objects.filter(pk=id)):
        record = Transaction.objects.filter(pk=id).first()
        his_balance = request.user.balance
        if record.transaction_type == "Income":
            if request.user.balance <= record.amount:
                messages.add_message(request, messages.ERROR, "Account balance Insufficient!")
                return redirect('records')
            else:
                his_balance -= record.amount
        else:
            his_balance += record.amount
        Transaction.objects.filter(pk=id).delete()
        request.user.balance = his_balance
        request.user.save()
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
        category = Category.objects.get(pk=id)
    except:
        messages.add_message(request, messages.ERROR, "Category could not be found!")
        return redirect('feed')

    if request.method == 'POST':
        form = CategoryDetailsForm(instance=category, data=request.POST)
        if (form.is_valid()):
            messages.add_message(request, messages.SUCCESS, "Category updated!")
            form.save()
            return redirect('feed')
        else:
            return render(request, 'edit_category_details.html', {'form': form, 'category': category})
    else:
        form = CategoryDetailsForm(instance=category)
        return render(request, 'edit_category_details.html', {'form': form, 'category': category})


def category(request):
    categories = get_categories(request.user)
    return render(request, 'category.html', {'categories': categories})


def view_category(request, id):
    try:
        category = Category.objects.get(pk=id)
    except:
        messages.add_message(request, messages.ERROR, "Category could not be found!")
        return redirect('feed')

    transactions = get_user_transactions(request.user)
    # category = Category.objects.get(category_id=category_id)
    context = {'category': category, 'transactions': transactions}
    return render(request, 'view_category.html', context)


def day_interval(start, end):
    """
    :param start:
    :param end:
    :return:
    """
    start = datetime.strptime(start, '%Y-%m-%d') + relativedelta(days=-1)
    end = datetime.strptime(end, '%Y-%m-%d')
    days = rrule.rrule(rrule.DAILY, dtstart=start, until=end)
    days = [day.strftime('%Y-%m-%d') for day in days]
    return days


def get_today(date):
    """

    """
    s_time = datetime.strptime(str(date)[:10] + '00:00:00', '%Y-%m-%d%H:%M:%S')
    e_time = datetime.strptime(str(date)[:10] + '23:59:59', '%Y-%m-%d%H:%M:%S')
    return s_time, e_time


def dashboard(request):
    transactions = list(get_user_transactions(request.user))
    from_date = ''
    to_date = ''
    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

    if not from_date or not to_date:
        to_date = datetime.now()
        from_date = to_date + relativedelta(days=-7)
        to_date = to_date.strftime('%Y-%m-%d')
        from_date = from_date.strftime('%Y-%m-%d')
    days_list = day_interval(from_date, to_date)
    # 当前余额
    now_balance = request.user.balance
    map_list = []
    for day in sorted(days_list, reverse=True):
        _transactions = [transaction for transaction in transactions if str(transaction.date_paid) == day]
        now_total_income = 0
        now_total_expense = 0
        for transaction in _transactions:
            if transaction.transaction_type == "Income":
                now_total_income += transaction.amount
            else:
                now_total_expense += transaction.amount
        map_list.append({
            "expense": now_total_expense,
            "income": now_total_income,
            "balance": now_balance
        })
        now_balance += now_total_expense - now_total_income
    result = []
    for index, day in enumerate(sorted(days_list, reverse=True)):
        if index + 1 == len(days_list):
            break
        now_balance = map_list[index]['balance']
        now_expense = map_list[index]['expense']
        now_income = map_list[index]['income']
        last_balance = map_list[index + 1]['balance']
        last_income = map_list[index + 1]['income']
        last_expense = map_list[index + 1]['expense']
        if last_balance:
            balance_rate = (now_balance - last_balance) / last_balance * 100
        else:
            balance_rate = (now_balance - last_balance) / 1
        if last_expense:
            expense_rate = (now_expense - last_expense) / last_expense * 100
        else:
            expense_rate = (now_expense - last_expense) / 1
        if last_income:
            income_rate = (now_income - last_income) / last_income * 100
        else:
            income_rate = (now_income - last_income) / 1
        income_rate = str(round(income_rate, 2)) + "%"
        expense_rate = str(round(expense_rate, 2)) + "%"
        balance_rate = str(round(balance_rate, 2)) + "%"
        result.append({
            "day": day,
            "income_rate": income_rate,
            "expense_rate": expense_rate,
            "balance_rate": balance_rate,
            "now_balance": float(now_balance),
            "now_expense": float(now_expense),
            "now_income": float(now_income)
        })
    return render(request, 'dashboard.html', {'result': result})
