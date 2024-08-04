from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.PositiveIntegerField(default=1000)
    investments = models.JSONField(default=dict)

    def __str__(self):
        return self.user.username
    