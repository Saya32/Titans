# Create your views here.

from spendingtrackers.forms import SignUpForm
from django.contrib.auth import login
from django.views.generic.edit import FormView
from django.urls import reverse
from spendingtrackers.helpers import set_achievements, update_achievements
from spendingtrackers.views.views import LoginProhibitedMixin





class SignUpView(LoginProhibitedMixin, FormView):
    """View that signs up user."""

    form_class = SignUpForm
    template_name = "sign_up.html"
    redirect_when_logged_in_url = 'sign_success'

    def form_valid(self, form):
        self.object = form.save()
        set_achievements(self.object)
        update_achievements(self.object)
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(self.redirect_when_logged_in_url)

