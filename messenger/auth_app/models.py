from django.contrib.auth.models import User
from django.db import models


def profile_avatar_directory_path(instance: "Profile", filename: str) -> str:
    return "profiles/profile_{pk}/avatar/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


class Profile(models.Model):
    avatar = models.ImageField(blank=True, upload_to=profile_avatar_directory_path)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    friends = models.ManyToManyField(User, related_name='user_friends', blank=True)

    def __str__(self):
        return self.username


class FriendRequest(models.Model):
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Friend request from {self.from_user.username} to {self.to_user.username}'
