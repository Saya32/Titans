from .models import User
from django.conf import settings
from django.shortcuts import redirect
from django.utils import timezone

class LogInTester:
    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()