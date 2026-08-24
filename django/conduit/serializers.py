from rest_framework import serializers
import conduit.models as models
from rest_framework_simplejwt.tokens import RefreshToken

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
        fields = ["email", "username", "bio", "image", "token"]

    token = serializers.SerializerMethodField("generate_token")

    def generate_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh.access_token)

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

class Article(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = ["slug", "title", "description", "body", "tagList", "createdAt", 
                  "updatedAt", "favoritesCount", "author"]

    favorited = serializers.SerializerMethodField("is_favorited")

    # check if current user has favorited the article
    def is_favorited(self, obj):
        # TODO
        return

class NewArticle(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = ["title, description, body, tagList"]
        extra_kwargs = {
            "tagList" : {"required": False},
        }

class UpdateArticle(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = ["title", "description", "body", "tagList"]
        extra_kwargs = {
            "title" : {"required": False},
            "description" : {"required": False},
            "body" : {"required": False},
            "tagList" : {"required": False},
        }

class Comment(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = "__all__"

class NewComment(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ["body"]
        