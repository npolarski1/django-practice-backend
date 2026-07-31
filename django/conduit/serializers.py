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

# used in UserResponse
class User(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["email", "username", "bio", "image"]

    token = serializers.SerializerMethodField

    def generate_token(self, obj):
        # TODO
        return