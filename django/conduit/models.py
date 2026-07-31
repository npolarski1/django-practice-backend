from django.db import models
from django.contrib.auth.models import User

class SiteUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=150, blank=True)
    image = models.CharField(max_length=150, blank=True)
    following = models.ManyToManyField("self", symmetrical=False)
