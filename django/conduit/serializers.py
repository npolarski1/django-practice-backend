from rest_framework import serializers
import models

class LoginUser(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["email", "password"]

class NewUser(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["username", "email", "password"]