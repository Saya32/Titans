# Create your views here.
import re
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from spendingtrackers.models import Transaction


@login_required
def delete_record(request, id):
    if (Transaction.objects.filter(pk=id)):
        Transaction.objects.filter(pk=id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted!")
        return redirect('feed')
    else:
        messages.add_message(request, messages.ERROR, "Sorry, an error occurred deleting your record.")
        return redirect('feed')

