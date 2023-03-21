# Create your views here.
import re
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import transaction
from spendingtrackers.helpers import get_user_transactions
from django.shortcuts import render
from datetime import datetime




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

