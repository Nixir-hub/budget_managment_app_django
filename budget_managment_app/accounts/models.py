from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    pass

class AccountBalance(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=5)

    def __str__(self):
        return f"{self.user.username} – {self.balance} zł"