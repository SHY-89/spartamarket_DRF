# Generated by Django 4.2 on 2024-09-04 07:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_user_birth_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="following",
            field=models.ManyToManyField(
                related_name="follow", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
