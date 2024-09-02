from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
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


class LoginAPIView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        res = super().post(request, *args, **kwargs)
        data = {
            "detail": "login success",
            "refresh": res.data.get('refresh', None),
            "access": res.data.get('access', None)
        }
        response = Response(data, status= status.HTTP_200_OK)
        response.set_cookie("refresh", res.data.get('refresh', None), httponly= True)
        response.set_cookie("access", res.data.get('access', None), httponly= True)

        return response
    

class LogoutAPIView(TokenBlacklistView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request: Request, *args, **kwargs) -> Response:
        refresh_token = request.COOKIES.get('refresh', 'Not Token')
        data = {"refresh": str(refresh_token)}
        serializer = self.get_serializer(data= data)

        try:
            serializer.is_valid(raise_exception= True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = Response({"detail": "token blacklisted"}, status= status.HTTP_200_OK)
        response.delete_cookie("refresh")
        response.delete_cookie("access")

        return response