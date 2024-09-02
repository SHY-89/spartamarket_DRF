from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer


# Create your views here.
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profil(request, username):
    user_info = get_object_or_404(User, username=username)
    if request.user == user_info:
        serializer = UserSerializer(user_info)
        return Response(serializer.data, status=200)
    return Response({"error":"본인계정만 조회가 가능합니다."}, status=400)