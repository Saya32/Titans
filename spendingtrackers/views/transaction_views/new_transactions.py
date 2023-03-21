# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from spendingtrackers.models import Transaction, Category
from django.contrib.auth.decorators import login_required
from spendingtrackers.forms import TransactionForm
from django.contrib import messages
from spendingtrackers.helpers import update_achievements
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from spendingtrackers.models import Transaction
from django.shortcuts import render


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



