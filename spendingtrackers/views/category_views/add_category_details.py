# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from spendingtrackers.forms import CategoryDetailsForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db import transaction




@transaction.atomic        #https://docs.djangoproject.com/en/4.1/topics/db/transactions/
@login_required
def add_category_details(request):
    try:
        if request.method == 'POST':
            form = CategoryDetailsForm(request.POST)
            if form.is_valid():
                category = form.save(commit=False)
                category.user = request.user
                category.save()
                messages.success(request, "Category added.")
                return redirect('category')
            else:
                messages.error(request, "Invalid form data.")
        else:
            form = CategoryDetailsForm()
        return render(request, 'add_category_details.html', {'form': form})
    except:
        with transaction.atomic(): #https://stackoverflow.com/questions/21458387/transactionmanagementerror-you-cant-execute-queries-until-the-end-of-the-atom
            messages.add_message(request, messages.ERROR, "Error: Category exists")
            return redirect('category')

