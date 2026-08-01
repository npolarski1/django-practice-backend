from psycopg import IntegrityError

import serializers

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(["POST"])
def create_user(request):
    serializer = serializers.NewUser(data=request.data)

    if serializer.is_valid():
        serializer.save()

        # TODO implement error handling (409/422 responses)

        return Response(serializers.User(serializer.data), status=status.HTTP_201_CREATED)
