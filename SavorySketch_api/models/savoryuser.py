from django.db import models
from django.contrib.auth.models import User

class SavoryUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_account")
    biography = models.CharField(max_length=750)
    profile_img = models.URLField(null=True, blank=True)
    created_on = models.DateField(auto_now=True)