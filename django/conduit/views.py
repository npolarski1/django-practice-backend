from psycopg import IntegrityError

import serializers

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from models import User
from django.db.models import Model

# /users
# Register a new user
@api_view(["POST"])
def create_user(request):
    serializer = serializers.NewUser(data=request.data)

    if serializer.is_valid():
        serializer.save()

        # TODO implement error handling (409/422 responses)

        return Response(serializers.User(serializer.data), status=status.HTTP_201_CREATED)

# /users/login
# Login for existing user
@api_view(["POST"])
def login(request):
    # convert json request data to serializer
    serializer = serializers.LoginUser(data=request.data)

    # validate data matches expected schema
    if serializer.is_valid():
        # Pylance doesn't know is_valid() populates validated_data so assert to silence error
        valid_data = serializer.validated_data
        assert isinstance(valid_data, dict)

        # check that user with inputted email exists
        try:
            user = User.objects.get(email=valid_data.get("email"))
        # if user doesn't exist, return 401 error code
        except Model.DoesNotExist:
            # TODO
            return Response()

        # check password matches
        if user.password == valid_data.get("password"):
            # TODO return with JWT
            return Response()
        else:
            # TODO return 408 error code
            return Response()

# /user
# Gets the currently logged-in user
@api_view(["GET"])
def get_current_user(request):

    # TODO get currently logged in user
    # 200 code for success
    # 401 if logged out
    # 422 for generic error?

    return Response()

# /user
# Update current user
@api_view(["PUT"])
def update_current_user(request):
    serializer = serializers.UpdateUser(data=request.data)

    if serializer.is_valid():
        # TODO
        # get current user
        # update user data with new data
        # save to db
        return Response()
    else:
        return Response()
        # 422 error

# /profiles/{username}
# Get a profile
@api_view(["GET"])
def get_profile_by_username(request):

    # TODO
    # get username param
    # 200 with ProfileResponse on success
    # 404 if profile doesn't exist
    # 422 for generic error
    return Response()

# /profiles/{username}/follow
# Follow a user
@api_view(["POST"])
def follow_user_by_username(request):
    # TODO
    # get user from username param
    # add user to following for logged in user
    # 200 with ProfileResponse on success
    # 401 if not logged in
    # 404 if profile doesn't exist
    # 422 for generic error
    return Response()

# /profiles/{username}/follow
# Unfollow a user
@api_view(["DELETE"])
def unfollow_user_by_username(request):
    # TODO
    # get user from username param
    # remove user from following list
    # save updated current user following list to db
    # return:
    #   200 with ProfileResponse on success
    #   401 if not logged in
    #   404 if profile doesn't exist
    #   422 if already unfollowed
    return Response()

# /articles
# Get recent articles globally
@api_view(["GET"])
def get_articles(request):
    # TODO
    # query db for articles and filter by query params
    # return:
    #   200 with MultipleArticlesResponse on sucess
    #   422 for generic error
    return Response()

# /articles
# Create an article
@api_view(["POST"])
def create_article(request):
    serializer = serializers.NewArticle(data=request.data)

    if serializer.is_valid():
        valid_data = serializer.validated_data
        # TODO
        # create new article from valid_data
        # save article to db
        # return:
        #   201 with SingleArticleResponse on success
        #   401 if not logged in
        #   409 if article with stub already exists
    else:
        # 422 for invalid data
        return Response()

# /articles/feed
# Get most recent articles from users you follow. Use query parameters to limit. Auth is required
@api_view(["GET"])
def get_articles_feed(request):
    # TODO
    # get followed users list for current user
    # get articles authored for each followed user
    # aggregate to build feed list
    # return:
    #   200 with MultipleArticlesResponse
    #   401 when not logged in
    #   422 for generic error
    return Response()

# /articles/{slug}
# Get an article. Auth not required
@api_view(["GET"])
def get_article(request):
    # TODO
    # get article with matching slug
    # return:
    #   200 with SingleArticleResponse
    #   404 if no article found
    #   422 for generic error
    return Response()

# /articles/{slug}
# Update an article. Auth is required
@api_view(["PUT"])
def update_article(request):
    serializer = serializers.UpdateArticle(data=request.data)

    if serializer.is_valid():
        valid_data = serializer.validated_data
        # TODO
        # get article with matching slug
        # update with valid_data
        # save to db
        # return:
        #   200 with SingleArticleResponse
        #   401 if not logged in
        #   403 if current user hasn't authored article
        #   404 if article not found
        return Response()
    # 422 for invalid data
    return Response()

# /articles/{slug}
# Delete an article. Auth is required
@api_view(["DELETE"])
def delete_article(request):
    # TODO
    # find article with matching slug in db
    # delete article from db
    # return:
    #   204 with EmptyOkResponse
    #   401 if not logged in
    #   403 if user hasn't authored article
    #   404 if article not found
    #   422 for generic error
    return Response()

# /articles/{slug}/comments
# Get the comments for an article. Auth is optional
@api_view(["GET"])
def get_article_comments(request):
    # TODO
    # get article with matching slug from db
    # get article's comments
    # return:
    #   200 with MultipleCommentsResponse
    #   401 if not logged in
    #   404 if article not found
    #   422 for generic error
    return Response()

# /articles/{slug}/comments
# Create a comment for an article. Auth is required
@api_view(["POST"])
def create_article_comment(request):
    serializer = serializers.NewComment(data=request.data)

    if serializer.is_valid():
        valid_data = serializer.validated_data

        # TODO
        # get article with matching slug from db
        # get comments for article
        # create comment from valid_data
        # add comment to article's comments
        # save to db
        # return:
        #   201 with SingleCommentResponse
        #   401 if not logged in
        #   404 if article not found
        return Response()
    # 422 for invalid data
    return Response()

# /articles/{slug}/comments/{id}
# Delete a comment for an article. Auth is required
@api_view(["DELETE"])
def delete_article_comment(request):
    # TODO
    # find comment from id in db
    # delete comment from db
    # return:
    #   204 with EmptyOkResponse
    #   401 if not logged in
    #   403 if user didn't author comment
    #   404 if article or comment doesn't exist
    #   422 for generic error
    return Response()

# /articles/{slug}/favorite
# Favorite an article. Auth is required
@api_view(["POST"])
def create_article_favorite(request):
    # TODO
    # get article with matching stub from db
    # add article to user's favorites
    # save user's favorites to db
    # return:
    #   200 with SingleArticleResponse
    #   401 if not logged in
    #   404 if article doesn't exist
    #   422 for generic error
    return Response()

# /articles/{slug}/favorite
# Unfavorite an article. Auth is required
@api_view(["DELETE"])
def delete_article_favorite(request):
    # TODO
    # get article with matching stub from db
    # get user's favorites from db
    # remove article from user's favorites
    # save to db
    # return:
    #   200 with SingleArticleResponse
    #   401 if not logged in
    #   404 if article doesn't exist
    #   422 for generic error
    return Response()
