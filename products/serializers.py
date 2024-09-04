from rest_framework import serializers
from .models import Product, Category

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        CATEGORY_CHOICE = []
        for category_info in Category.objects.all():
            CATEGORY_CHOICE.append(category_info.pk)
        model = Product
        fields = ("title", "content", "image", "category")
        category = serializers.ChoiceField(choices=CATEGORY_CHOICE)



class SelectProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"