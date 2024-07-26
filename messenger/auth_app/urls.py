from django.urls import path
from .views import SignUpView, SingInView, SignOutView, LoggedInUser, ProfileInfoView, UsersListView, \
    FriendsRequestsView, ConfirmAddToFriendsList, SendFriendRequest, DeleteFriendView, UpdateAvatarView, \
    UpdateProfileDataView

app_name = "auth_app"

urlpatterns = [
    path('', LoggedInUser.as_view(), name='current_user'),
    path('user/change/avatar', UpdateAvatarView.as_view(), name='change_avatar'),
    path('register', SignUpView.as_view(), name='sign_up'),
    path('login', SingInView.as_view(), name='sign_in'),
    path('logout', SignOutView.as_view(), name='logout'),
    path('user/<int:pk>', ProfileInfoView.as_view(), name='profile_info'),
    path('users/', UsersListView.as_view(), name='users_list'),
    path('user/change/data', UpdateProfileDataView.as_view(), name='change_data'),

    path('user/<int:pk>/friend', SendFriendRequest.as_view(), name='send_friend_request'),
    path('friends/requests', FriendsRequestsView.as_view(), name="friends_requests"),
    path('friends/requests/confirm/<int:pk>', ConfirmAddToFriendsList.as_view(), name='confirm_friend'),
    path('friends/delete/<int:pk>', DeleteFriendView.as_view(), name='delete_friend'),
]
