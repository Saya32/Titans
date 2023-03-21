# Create your views here.
from spendingtrackers.models import Transaction
from django.http import JsonResponse



def chart_income_graph(request):
    # Retrieve user's transactions
    transactions = Transaction.objects.filter(user=request.user).order_by('date_paid')
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
