from django.contrib import admin

from auth_app.models import Profile, FriendRequest


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fields = 'avatar', 'friends', 'name', 'email', 'username'


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'created_at']
