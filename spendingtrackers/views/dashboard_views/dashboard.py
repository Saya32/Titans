# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from spendingtrackers.views.dashboard_views.chart_balance_graph import chart_balance_graph
from spendingtrackers.views.dashboard_views.chart_expense_graph import chart_expense_graph, chart_income_graph, expense_structure
from spendingtrackers.views.dashboard_views.expense_structure import expense_structure2



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

