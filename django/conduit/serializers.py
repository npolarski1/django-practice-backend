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

    token = serializers.SerializerMethodField("generate_token")

    def generate_token(self, obj):
        # TODO
        return

class UpdateUser(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["email", "password", "username", "bio", "image"]
        extra_kwargs = {
            "bio" : {"required": False},
            "image" : {"required": False},
        }

class Profile(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["bio, image, username"]

    following = serializers.SerializerMethodField("is_following")

    # checks if the current user is following the profile
    def is_following(self, obj):
        # TODO
        return