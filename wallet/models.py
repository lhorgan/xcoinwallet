from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet_account = models.CharField(max_length=1000)
    wallet_password = models.CharField(max_length=1000)
    public_key = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.user) + " (" + self.public_key + ")"