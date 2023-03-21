# Create your views here.
from django.shortcuts import redirect
from ..models import Category
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..helpers import delete_transactions



@login_required
def delete_category(request, id):
    if (Category.objects.filter(pk=id)):
        category = Category.objects.filter(pk=id)
        delete_transactions(request.user, category)
        Category.objects.filter(pk=id).delete()
        messages.add_message(request, messages.SUCCESS, "Category deleted!")
        return redirect('feed')
    else:
        messages.add_message(request, messages.ERROR, "Sorry, an error occurred deleting your Category")
        return redirect('feed')

