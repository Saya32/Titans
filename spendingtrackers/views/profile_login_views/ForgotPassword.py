# Create your views here.
import re
from django.shortcuts import render
from spendingtrackers.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password


def forgot_password(request):
    if request.method == 'POST':
        user_name = request.POST['email']
        pin = request.POST['pin']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']
        regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$'
        if not re.match(regex, password):
            messages.add_message(request, messages.ERROR, 'Password must contain an uppercase character, a lowercase '
                                                          'character and a number')
            return render(request, 'forgot_password.html')
        user = User.objects.filter(username__exact=user_name).first()
        if not user:
            messages.add_message(request, messages.ERROR, "email does not exist!")
            return render(request, 'forgot_password.html')
        if user.pin != pin:
            messages.add_message(request, messages.ERROR, "pin error!")
            return render(request, 'forgot_password.html')
        if password != password_confirmation:
            messages.add_message(request, messages.ERROR, "The two passwords are inconsistent!")
            return render(request, 'forgot_password.html')
        user.password = make_password(password)
        user.save()
        messages.add_message(request, messages.SUCCESS, "SUCCESS!")
        return render(request, 'forgot_password.html')
    else:
        return render(request, 'forgot_password.html')
