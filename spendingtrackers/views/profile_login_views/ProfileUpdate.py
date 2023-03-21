# Create your views here.
from django.conf import settings
from django.urls import reverse
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from spendingtrackers.forms import UserForm



class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """View to update logged-in user's profile."""
    model = UserForm
    template_name = "profile.html"
    form_class = UserForm

    def get_object(self):
        """Return the object (user) to be updated."""
        user = self.request.user
        return user

    def get_success_url(self):
        """Return redirect URL after successful update."""
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)