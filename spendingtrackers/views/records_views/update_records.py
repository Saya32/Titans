# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from spendingtrackers.models import Transaction, Category
from django.contrib.auth.decorators import login_required
from spendingtrackers.forms import TransactionForm
from django.contrib import messages
from spendingtrackers.models import Transaction
from django.shortcuts import render


@login_required
def update_record(request, id):
    try:
        record = Transaction.objects.get(pk=id)
    except:
        messages.add_message(request, messages.ERROR, "Record could not be found!")
        return redirect('feed')

    
    if request.method == 'POST':
        form = TransactionForm(instance=record, data=request.POST)
        if (form.is_valid()):
            
            try:
                category_name = form.cleaned_data['category']
                category_object = get_object_or_404(Category, user=request.user, name=category_name)
            except:
                messages.add_message(request, messages.ERROR, "Category could not be found!")
                return redirect('feed')
            
            messages.add_message(request, messages.SUCCESS, "Record updated!")
            form.save()
            record = Transaction.objects.get(pk=id)
            record.category_fk = category_object
            record.save()
            return redirect('feed')
        else:
            return render(request, 'update_record.html', {'form': form, 'transaction': record})
    else:
        form = TransactionForm(instance=record)
        return render(request, 'update_record.html', {'form': form, 'transaction': record})

