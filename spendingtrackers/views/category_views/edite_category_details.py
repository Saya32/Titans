# Create your views here.
import re
from django.shortcuts import render, redirect
from spendingtrackers.models import Category
from django.contrib.auth.decorators import login_required
from spendingtrackers.forms import CategoryDetailsForm
from django.contrib import messages
from spendingtrackers.helpers import change_transaction_name
from django.shortcuts import render



@login_required
def edit_category_details(request, id):
    try:
        category = Category.objects.get(pk=id, user=request.user)
    except:
        messages.add_message(request, messages.ERROR, "Category could not be found!")
        return redirect('category')

    if request.method == 'POST':
        form = CategoryDetailsForm(instance=category, data=request.POST)
        if (form.is_valid()):
            change_transaction_name(request.user, category)
            messages.add_message(request, messages.SUCCESS, "Category updated!")
            form.save()
            return redirect('category')
        else:
            return render(request, 'edit_category_details.html', {'form': form, 'category': category})
    else:
        form = CategoryDetailsForm(instance=category)
        return render(request, 'edit_category_details.html', {'form': form, 'category': category})

