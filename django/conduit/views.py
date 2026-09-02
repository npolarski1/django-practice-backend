import conduit.serializers as serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from conduit.models import User
from django.db.models import Model
import logging

# /users
# Register a new user
@api_view(["POST"])
def create_user(request):
    # pass in empty dict to get() in case of bad request because serializer expects dict
    serializer = serializers.NewUser(data=request.data.get("user", {}))

    if serializer.is_valid():
        valid_data = serializer.validated_data
        assert isinstance(valid_data, dict) # to silence Pylance

        new_user = User(**valid_data)
        # set_password hashes the password
        new_user.set_password(valid_data.get("password"))

        # save to db and return 201 on success
        new_user.save()
        return Response({"user": serializers.User(new_user).data}, status=status.HTTP_201_CREATED)
    else:
        logging.error(f"Invalid request: {serializer.errors}")

        assert isinstance(serializer.errors, dict) # silence Pylance, we know errors is populated

        # return 409 if user already exists
        if username_errors := serializer.errors.get("username"):
            if username_errors[0].code == "unique":
                return Response({"errors": serializer.errors}, status=status.HTTP_409_CONFLICT)
        if email_errors := serializer.errors.get("email"):
            if email_errors[0].code == "unique":
                return Response({"errors": serializer.errors}, status=status.HTTP_409_CONFLICT)

        # return 422 error for other errors
        return Response({"errors": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

# /users/login
# Login for existing user
@api_view(["POST"])
def login(request):
    # convert json request data to serializer
    serializer = serializers.LoginUser(data=request.data.get("user", {}))

    # validate data matches expected schema
    if serializer.is_valid():
        # Pylance doesn't know is_valid() populates validated_data so assert to silence error
        valid_data = serializer.validated_data
        assert isinstance(valid_data, dict)

        # check that user with inputted email exists
        try:
            user = User.objects.get(email=valid_data.get("email"))
        # if email is wrong, return 401 error code
        except Model.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response({"user": serializers.User(user).data}, status=status.HTTP_200_OK)
    else:
        assert isinstance(serializer.errors, dict) # silence Pylance, we know errors is populated

        logging.error(f"Invalid request: {serializer.errors}")

        # return 422 by default 
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

        # return 401 for invalid password
        if password_errors := serializer.errors.get("password"):
            if password_errors[0].code == "invalid":
                status_code = status.HTTP_401_UNAUTHORIZED
                return Response({"errors": {"credentials": ["invalid"]}}, status_code)

        return Response({"errors": serializer.errors}, status_code)

# /user
@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def current_user(request):
    # Gets the currently logged-in user
    if request.method == "GET":
        return Response({"user": serializers.User(request.user).data}, status=status.HTTP_200_OK)
    # Update current user
    elif request.method == "PUT":
        serializer = serializers.UpdateUser(data=request.data.get("user", {}))
        
        if serializer.is_valid():
            valid_data = serializer.validated_data
            assert isinstance(valid_data, dict)
            
            # get current user
            user = request.user

            # update user data with new data
            if "email" in valid_data:
                user.email = valid_data["email"]
            if "username" in valid_data:
                user.username = valid_data["username"]
            if "password" in valid_data:
                user.password = valid_data["password"]
            if "bio" in valid_data:
                user.bio = valid_data["bio"]
            if "image" in valid_data:
                user.image = valid_data["image"]

            # save to db
            user.save(update_fields=["username", "password", "bio", "image", "email"])

            return Response({"user": serializers.User(user).data}, status=status.HTTP_200_OK)
        else:
            # return 422 for invalid data
            logging.error(f"Invalid request schema: {serializer.errors}")
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

# /profiles/{username}
# Get a profile
@api_view(["GET"])
def get_profile_by_username(request, username):

    profile_user = User.objects.get(username=username)

    # 200 with ProfileResponse on success
    # pass request.user as context for checking if they follow profile_user
    profile = serializers.Profile(profile_user, context={"request_user": request.user})
    return Response(data={"profile": profile.data}, status=status.HTTP_200_OK)

    # 404 if profile doesn't exist
    # 422 for generic error

# /profiles/{username}/follow
# Follow a user
@api_view(["POST", "DELETE"])
def follow_unfollow_user_by_username(request, username):
    # get user from username URL param
    profile_user = User.objects.get(username=username)

    # /profiles/{username}/follow
    if request.method == "POST":
        request.user.followed_users.add(profile_user)

        # need to pass user as context to add profile_user to set is_following
        profile = serializers.Profile(profile_user, context={"request_user": request.user})

        # 200 with ProfileResponse on success
        return Response(data={"profile": profile.data}, status=status.HTTP_200_OK)

        # 401 if not logged in
        # 404 if profile doesn't exist
        # 422 for generic error
    
    # Unfollow a user
    elif request.method == "DELETE":
        request.user.followed_users.remove(profile_user)

        profile = serializers.Profile(profile_user, context={"request_user": request.user})

        # return 200 with ProfileResponse on success
        return Response(data={"profile": profile.data}, status=status.HTTP_200_OK)

        #   401 if not logged in
        #   404 if profile doesn't exist
        #   422 if already unfollowed

# /articles
@api_view(["GET", "POST"])
def get_create_articles(request):
    # Get recent articles globally
    if request.method == "GET":
        # TODO
        # query db for articles and filter by query params
        # return:
        #   200 with MultipleArticlesResponse on sucess
        #   422 for generic error
        return Response()
    # Create an article
    elif request.method == "POST":
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
@api_view(["GET", "PUT", "DELETE"])
def get_update_delete_article(request):
    # Get an article. Auth not required
    if request.method == "GET":
        # TODO
        # get article with matching slug
        # return:
        #   200 with SingleArticleResponse
        #   404 if no article found
        #   422 for generic error
        return Response()
    # Update an article. Auth is required
    elif request.method == "PUT":
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
    # Delete an article. Auth is required
    elif request.method == "DELETE":
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
@api_view(["GET", "POST"])
def get_addto_article_comments(request):
    # Get the comments for an article. Auth is optional
    if request.method == "GET":
        # TODO
        # get article with matching slug from db
        # get article's comments
        # return:
        #   200 with MultipleCommentsResponse
        #   401 if not logged in
        #   404 if article not found
        #   422 for generic error
        return Response()
    # Create a comment for an article. Auth is required
    elif request.method == "POST":
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
@api_view(["POST", "DELETE"])
def create_delete_article_favorite(request):
    # Favorite an article. Auth is required
    if request.method == "POST":
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
    # Unfavorite an article. Auth is required
    elif request.method == "DELETE":
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

# /tags
# Get tags. Auth not required
@api_view(["GET"])
def get_tags(request):
    # TODO
    # return:
    #   200 with TagsResponse
    #   422 for generic error
    return Response()
