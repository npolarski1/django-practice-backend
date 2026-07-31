from rest_framework import serializers
import models

class LoginUser(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["email", "password"]