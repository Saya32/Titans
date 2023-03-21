# Create your views here.
from spendingtrackers.models import Transaction
from django.http import JsonResponse

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
            expense = 0
        data.append(float(expense))
    # Create chart data
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
