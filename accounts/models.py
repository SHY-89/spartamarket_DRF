from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', '남성'),
        ('F', '여성'),
    )
    name = models.CharField(max_length=10)
    nickname = models.CharField(max_length=10)
    email = models.EmailField(_("email address"), unique=True)
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    memo = models.TextField(blank=True)

    def __str__(self):
        return self.username