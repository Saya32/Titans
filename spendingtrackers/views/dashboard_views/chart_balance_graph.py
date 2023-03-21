# Create your views here.
from spendingtrackers.models import Transaction
from django.http import JsonResponse



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
        data.append(int(balance))
    
    # Create chart data
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
    