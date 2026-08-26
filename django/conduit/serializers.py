from rest_framework import serializers
import conduit.models as models
from rest_framework_simplejwt.tokens import RefreshToken

class LoginUser(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class NewUser(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["username", "email", "password"]
        extra_kwargs = {
            "username": {
                "error_messages": {
                    "blank": "can't be blank"
                }
            },
            "email": {
                "error_messages": {
                    "blank": "can't be blank"
                }
            }
        }

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
            "email": {"required": False},
            "password": {"required": False},
            "username": {"required": False},
            "bio" : {"required": False},
            "image" : {"required": False},
        }

    def validate(self, attrs):
        # validate at least one user attribute is being updated
        if not any(field in attrs for field in self.fields):
            raise serializers.ValidationError("No user attributes specified to be updated")
        
        return attrs

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
        