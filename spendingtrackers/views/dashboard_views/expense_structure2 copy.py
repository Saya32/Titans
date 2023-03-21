# Create your views here.
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from spendingtrackers.models import Transaction
from django.http import JsonResponse


def expense_structure2(request):
    # Retrieve user's transactions
    transactions = Transaction.objects.filter(user=request.user).order_by('category')
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

