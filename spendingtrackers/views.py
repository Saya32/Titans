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
from django.views.generic.edit import  UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .helpers import get_user_transactions, get_categories
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
import csv
from django.shortcuts import render
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd
import numpy as np
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import BytesIO
import base64
from django.http import JsonResponse
from django.db.models import Sum
from spendingtrackers.models import Transaction
import datetime 
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
import pandas as pd



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
                #category_fk= request.user.get_category(form.cleaned_data.get('category'))
            )
            return redirect('feed')
        else:
            return render(request, 'new_transaction.html', {'form': form})
    else:
        form = TransactionForm()
        return render(request, 'new_transaction.html', {'form': form})


def records(request):
    transactions = get_user_transactions(request.user)
    return render(request, 'records.html', {'transactions' : transactions})

#def records_csv(request):
 #   response = HttpResponse(content_type='text/csv', headers={'Content-Disposition': 'attachment; filename="records.csv"'},)
    #create writer
  #  writer = csv.writer(response)
    #designate model
   # records = Transaction.objects.all()
    #add column headings
    #writer.writerow(['Amount'])
    #loop through and output
    #for record in records:
     #   writer.writerow([Transaction.amount])

    #return response

#@login_required
#def chart_balance_graph(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user).order_by('date_paid', 'time_paid')
    if transactions:
        dates = []
        balance = []
        total_balance = 0
        for transaction in transactions:
            total_balance += transaction.amount
            dates.append(transaction.date_paid)
            balance.append(total_balance)
        fig, ax = plt.subplots()
        ax.plot(dates, balance)
        ax.set(xlabel='Date', ylabel='Balance', title='Balance Trends')
        ax.grid()
        # Convert the figure to a PNG string buffer
        buffer = BytesIO()
        fig.savefig(buffer, format='png')
        buffer.seek(0)
        # Encode the PNG string buffer to base64 and include in the HTML response
        graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return render(request, 'dashboard.html', {'graph': graph})
    else:
        return render(request, 'dashboard.html')

#class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # Get the user's transactions
        transactions = Transaction.objects.filter(user=request.user)

        # Convert the transactions to a Pandas DataFrame
        df = pd.DataFrame(list(transactions.values()))

        # Calculate the balance for each date
        balance = df.groupby('date_paid')['amount'].sum().cumsum()

        # Create the line graph
        fig, ax = plt.subplots()
        ax.plot(balance.index, balance.values)
        ax.set_title('Balance Trends')
        ax.set_xlabel('Date')
        ax.set_ylabel('Balance')
        ax.grid()

        # Convert the graph to a PNG image
        canvas = FigureCanvasAgg(fig)
        response = HttpResponse(content_type='image/png')
        canvas.print_png(response)

        # Return the image
        return response


#def chart_balance_graph(request):
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
    chart_data = {
        'labels': labels,
        'datasets': [{
            'label': 'Balance',
            'data': data,
            'fill': False,
            'borderColor': 'rgb(75, 192, 192)',
            'lineTension': 0.1
        }]
    }
    
    # Pass chart data to template
    return render(request, 'dashboard.html', {'chart_data': json.dumps(chart_data)})

#def chart_balance_graph(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user).order_by('-date_paid')
    
    # Create a dictionary to store the balance for each date
    balance_dict = {}
    balance = 0
    for transaction in transactions:
        if transaction.transaction_type == 'Expense':
            balance -= transaction.amount
        else:
            balance += transaction.amount
        balance_dict[transaction.date_paid] = balance
    
    # Create a list of dates and corresponding balances for plotting
    date_list = []
    balance_list = []
    start_date = datetime.today() - timedelta(days=30)
    for i in range(30):
        date = start_date + timedelta(days=i)
        date_list.append(date.strftime('%m/%d'))
        balance = balance_dict.get(date.date(), balance)
        balance_list.append(balance)
    
    # Create and save the plot as a PNG image
    plt.plot(date_list, balance_list)
    plt.xlabel('Date')
    plt.ylabel('Balance')
    plt.title('Balance Trends')
    plt.savefig('balance.png')
    
    # Render the template with the plot image
    return render(request, 'dashboard.html', {'balance_graph': 'balance.png'})


def get_balance_data(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user)
    today = timezone.now().date()
    balance_data = []
    balance = 0
    for i in range(21):
        date = today - timedelta(days=i)
        transactions_on_date = transactions.filter(date_paid=date)
        for t in transactions_on_date:
            if t.transaction_type == 'Expense':
                balance -= t.amount
            else:
                balance += t.amount
        balance_data.append((date.strftime('%m/%d/%Y'), balance))
    return balance_data[::-1] # reverse the list so that the latest data is first

#def index(request):
    qs = Chart.objects.all()
    projects_data = [
        {
            'Project': x.name,
            'Start': x.start_date,
            'Finish': x.finish_date,
            'Responsible': x.responsible.username
        } for x in qs
    ]
    df = pd.DataFrame(projects_data)
    fig = px.timeline(
        df, x_start="Start", x_end="Finish", y="Project", color="Responsible"
    )
    fig.update_yaxes(autorange="reversed")
    gantt_plot = plot(fig, output_type="div")
    context = {'plot_div': gantt_plot}
    return render(request, 'index.html', context)

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
        category = Category.objects.get(pk=id)
    except:
        messages.add_message(request, messages.ERROR, "Category could not be found!")
        return redirect('feed')

    if request.method == 'POST':
        form = CategoryDetailsForm(instance = category, data = request.POST)
        if (form.is_valid()):
            messages.add_message(request, messages.SUCCESS, "Category updated!")
            form.save()
            return redirect('feed')
        else:
            return render(request, 'edit_category_details.html', {'form': form, 'category' : category})
    else:
        form = CategoryDetailsForm(instance = category)
        return render(request, 'edit_category_details.html', {'form': form, 'category' : category})

def category(request):
   categories = get_categories(request.user)
   return render(request, 'category.html', {'categories':categories})

def view_category(request, id):
    try:
        category = Category.objects.get(pk=id)
    except:
        messages.add_message(request, messages.ERROR, "Category could not be found!")
        return redirect('feed')

    transactions = get_user_transactions(request.user)
    #category = Category.objects.get(category_id=category_id)
    context = {'category': category, 'transactions': transactions}
    return render(request, 'view_category.html', context)

def dashboard(request):
    balance_data = get_balance_data(request)
    context = {
        'balance_data': balance_data,
        # other context variables
    }
    return render(request, 'dashboard.html')
