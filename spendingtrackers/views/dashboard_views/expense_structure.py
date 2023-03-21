# Create your views here.
from spendingtrackers.models import Transaction
from django.http import JsonResponse



def expense_structure(request):
    # Retrieve user's transactions
    transactions = Transaction.objects.filter(user=request.user).order_by('category')
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
