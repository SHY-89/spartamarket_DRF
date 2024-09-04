from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class HashTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    image = models.ImageField(upload_to="p_image/", default="media/p_image/zep.png")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="product")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    like_user = models.ManyToManyField( get_user_model(), related_name="like_product")
    hashtag = models.ManyToManyField(HashTag, related_name="hash_product")