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
