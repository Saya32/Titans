# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from spendingtrackers.helpers import get_achievements




@login_required
def view_achievements(request):
   achievements = get_achievements(request.user.id)
   return render(request, 'view_achievements.html', {'achievements':achievements})