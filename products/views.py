from django.core import serializers
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .models import Product
from .serializers import ProductSerializer


class ProductAPIView(APIView):
    def get(self, request):
        articles = Product.objects.all()
        serializer = ProductSerializer(articles, many=True)
        return Response(serializer.data)

    @permission_classes([IsAuthenticated])
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=201)
        

class ProductDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Product, pk=pk)

    def get(self, request, productId):
        product = self.get_object(productId)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, productId):
        product = self.get_object(productId)
        if product.author.username == request.user.username:
            serializer = ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        return Response({'error':'작성자만 수정이 가능합니다.'}, status=400)

    def delete(self, request, productId):
        product = self.get_object(productId)
        if product.author == request.user:
            product.delete()
            data = {"pk": f"{productId} is deleted."}
            return Response(data, status=200)
        return Response({'error':'작성자만 삭제 할 수 있습니다.'}, status=400)