from django.db import models
from django.contrib.postgres.fields import ArrayField

class User(models.Model):
    username = models.CharField()
    email = models.CharField()
    password = models.CharField()
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
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="authored_articles")
    favorited_by = models.ManyToManyField(User, related_name="favorite_articles")

class Comment(models.Model):
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()
    body = models.CharField(max_length=5000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)