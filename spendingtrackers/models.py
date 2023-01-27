from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class User(AbstractUser):
    """User model used for authentication and lessons authoring."""
    username = models.EmailField(
        unique=True,
        blank = False,
        )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)