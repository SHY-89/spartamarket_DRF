from django.core import serializers
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from .models import Product, Category, HashTag
from .serializers import ProductSerializer, SelectProductSerializer



class ProductAPIView(APIView):
    def get(self, request):
        # try:
        #     page = request.query_params.get("page", 1)
        #     page = int(page)
        # except ValueError:
        #     page = 1

        # page_size = 20
        # start = (page - 1) * page_size
        # end = start + page_size
        if request.query_params.get('serch_type') in ['title', 'content', 'user'] and request.query_params.get('serch_txt'):
            serch_type = request.query_params.get('serch_type')
            serch_txt = request.query_params.get('serch_txt')
            if serch_type == 'title':
                product = Product.objects.filter(title__icontains=serch_txt).order_by("-pk")
            elif serch_type == 'content':
                product = Product.objects.filter(content__icontains=serch_txt).order_by("-pk")
            elif serch_type == 'user':
                product = Product.objects.filter(author__username__icontains=serch_txt).order_by("-pk")
        else:
            product = Product.objects.all().order_by("-pk")
        paginator = Paginator(product, 20)
        page = request.query_params.get("page", 1)
        products = paginator.get_page(page)
        serializer = SelectProductSerializer(products, many=True)
        return Response(serializer.data)

    @permission_classes([IsAuthenticated])
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            category = get_object_or_404(Category, pk=request.data['category'])
            product = serializer.save(author=request.user)
            hashtags = request.data['hashtags'].replace(" ","").split(",")
            for tag in hashtags:
                if tag == "": continue
                tag = tag.title()
                hashtag, created = HashTag.objects.get_or_create(name=tag)
                if hashtag.pk not in product.hashtag.all():
                    product.hashtag.add(hashtag.pk)
            
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
                product = serializer.save()
                hashtags = request.data['hashtags'].replace(" ","").split(",")
                for tag in hashtags:
                    if tag == "": continue
                    tag = tag.title()
                    hashtag, created = HashTag.objects.get_or_create(name=tag)
                    if product.hashtag.filter(pk=hashtag.pk).exists():
                        product.hashtag.remove(hashtag.pk)
                    else:
                        product.hashtag.add(hashtag.pk)
                return Response(serializer.data)
        return Response({'error':'작성자만 수정이 가능합니다.'}, status=400)

    def delete(self, request, productId):
        product = self.get_object(productId)
        if product.author == request.user:
            product.delete()
            data = {"pk": f"{productId} is deleted."}
            return Response(data, status=200)
        return Response({'error':'작성자만 삭제 할 수 있습니다.'}, status=400)
    
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def like(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    message = {}
    status = 201
    if product.author.pk != request.user.pk:
        if product.like_user.filter(pk=request.user.pk):
            product.like_user.remove(request.user.pk)
            message['detile'] = "취소 되었습니다"
        else:
            product.like_user.add(request.user.pk)
            message['detile'] = "처리 되었습니다"
    else:
        message['error'] = "본이 작성한 물품은 찜할 수 없습니다."
        status = 400
    return Response(message, status=status)