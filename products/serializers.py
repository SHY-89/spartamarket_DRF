from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("title", "content", "image")


class SelectProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"