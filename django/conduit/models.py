from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class SiteUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=150, blank=True)
    image = models.CharField(max_length=150, blank=True)
    following = models.ManyToManyField("self", symmetrical=False)

class Article(models.Model):
    slug = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    body = models.CharField(max_length=100000)
    tagList = ArrayField(models.CharField(max_length=25), size=4)
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()
    favorites_count = models.IntegerField(default=0)
    author = models.ForeignKey(SiteUser, on_delete=models.CASCADE)

class Comment(models.Model):
    id = models.IntegerField()
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()
    body = models.CharField(max_length=5000)
    author = models.ForeignKey(SiteUser, on_delete=models.CASCADE)