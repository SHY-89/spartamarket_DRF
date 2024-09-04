from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.contrib.auth.hashers import check_password
import re
from .models import User
from .serializers import UserSerializer, UserProfilSerializer


# Create your views here.
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def password_change(request, username):
    user_info = get_object_or_404(User, username=username)
    if check_password(request.data['old_password'], user_info.password):
        if request.data['new_password1'] == request.data['new_password2']:
            password = request.data['new_password1']
            error = ""
            if len(password) < 8:
                error = "비밀번호는 8자리 이상이어야 합니다."
            if not re.search(r"[a-zA-Z]", password):
                error = "비밀번호는 하나 이상의 영문이 포함되어야 합니다."
            if not re.search(r"\d", password):
                error = "비밀번호는 하나 이상의 숫자가 포함되어야 합니다."
            if not re.search(r"[!@#$%^&*()]", password):
                error = "비밀번호는 적어도 하나 이상의 특수문자(!@#$%^&*())가 포함되어야 합니다."
            
            if error == "":
                user_info.set_password(password)
                user_info.save()
                return Response({'detail':'패스워드가 변경되었습니다'}, status=200)   
        else:
            error = '변경하시려는 패스워드가 서로 다릅니다.'
    else:
        error = "변경전 패스워드가 다릅니다."
    return Response({'error':error}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like(request, user_pk):
    serch_user = get_object_or_404(User, pk=user_pk)
    message = {}
    status = 201
    print(request.user.pk, serch_user.pk)
    if serch_user.pk != request.user.pk:
        if serch_user.following.filter(pk=request.user.pk):
            serch_user.following.remove(request.user.pk)
            message['detile'] = "취소 되었습니다"
        else:
            serch_user.following.add(request.user.pk)
            message['detile'] = "처리 되었습니다"
    else:
        message['error'] = "본인은 본인을 팔로우 할 수 없습니다."
        status = 400
    return Response(message, status=status)

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
    

class UserProfilAPIView(APIView):
    permission_classes =[IsAuthenticated]

    def get_user(self, username):
        return get_object_or_404(User, username=username)

    def get(self, request, username):
        user_info = self.get_user(username)
        if request.user == user_info:
            serializer = UserSerializer(user_info)
            return Response(serializer.data, status=200)
        return Response({"error":"본인계정만 조회가 가능합니다."}, status=400)
    
    def put(self, request, username):
        user_info = self.get_user(username)
        if request.user == user_info:
            serializer = UserProfilSerializer(user_info, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=200)
        return Response({"error":"본인계정만 수정 가능합니다."}, status=400)
    
    def delete(self, request, username):
        user_info = self.get_user(username)
        if user_info == request.user:
            if check_password(request.data['password'], user_info.password):
                user_info.delete()
                return Response({"detail": "회원 탈퇴가 정상적으로 되었습니다"}, status= status.HTTP_200_OK)
            else:
                return Response({'error':'패스워드가 다릅니다.'}, status=400)        
        return Response({'error':'본인계정만 탈퇴 할 수 있습니다.'}, status=400)