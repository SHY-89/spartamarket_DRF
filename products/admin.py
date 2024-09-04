from django.contrib import admin
from .models import Category, HashTag, Product

# Register your models here.
admin.site.register(Category)
admin.site.register(HashTag)
admin.site.register(Product)