# Generated by Django 4.2.14 on 2024-07-25 08:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth_app', '0002_friendrequest_profile_friends_profile_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='user_friends', to=settings.AUTH_USER_MODEL),
        ),
    ]
