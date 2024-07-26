from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View

from auth_app.forms import SignUpForm, SignInForm
from auth_app.models import Profile

from auth_app.models import FriendRequest

from auth_app.utils.validators import check_if_ppl_are_friends

from auth_app.forms import AvatarForm, UpdateProfileInfoForm


class LoggedInUser(View):
    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user.pk)
            friends = profile.friends.all()
            return render(request, 'auth/user_info.html', {"profile": profile, "friends": friends})
        except ObjectDoesNotExist:
            return render(request, 'auth/user_info.html', {"err_message": 'user is anonymous'})


class ProfileInfoView(View):
    def get(self, request, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            friends = profile.friends.all()
            is_friends = check_if_ppl_are_friends(profile, Profile.objects.get(user=request.user.id))
            return render(request, 'auth/profile_info.html',
                          {"profile": profile, "friends": friends, "is_friends": is_friends})
        except ObjectDoesNotExist:
            return render(request, 'auth/profile_info.html', {"err_message": "No profile found"})


class SignUpView(View):
    def post(self, request):
        form = SignUpForm(request.POST)
        try:
            if form.is_valid():
                email = form.cleaned_data['email']
                name = form.cleaned_data['name']
                username = form.validate_username()
                password = form.validate_password()
                user = form.save()
                profile = Profile.objects.create(user=user, name=name, username=username, email=email)
                profile.save()
                login(request, user)
                authenticate(username=username, password=password)
                success_url = reverse_lazy('auth_app:current_user')
                return HttpResponseRedirect(success_url)
            raise Exception
        except Exception as ex:
            error_url = reverse_lazy('auth_app:sign_up')
            return HttpResponseRedirect(error_url)

    def get(self, request):
        form = SignUpForm()
        return render(request, "auth/sign_up.html", {"form": form})


class SingInView(View):
    def post(self, request):
        success_url = reverse_lazy('auth_app:current_user')
        form = SignInForm(request.POST)
        if form.is_valid():
            user = form.validate_user()
            login(request, user)
            return HttpResponseRedirect(success_url)

    def get(self, request):
        form = SignInForm()
        return render(request, "auth/sign_in.html", {"form": form})


class SignOutView(View):
    def post(self, request):
        logout(request)
        return redirect('/')

    def get(self, request):
        return render(request, 'auth/logout.html', {})


class UsersListView(View):
    def get(self, request):
        users_list = Profile.objects.all()
        context = {'profiles': users_list}
        return render(request, 'auth/users_list.html', context)


class SendFriendRequest(View):
    def post(self, request, pk):
        if Profile.objects.get(pk=pk).user == request.user:
            return HttpResponse('You cant add yourself to friends', status=400)
        friend_request, created = FriendRequest.objects.get_or_create(to_user=Profile.objects.get(pk=pk).user,
                                                                      from_user=request.user)
        friend_request.save()
        success_url = reverse('auth_app:profile_info', kwargs={"pk": pk})
        return HttpResponseRedirect(success_url)

    def get(self, request, pk):
        return render(request, 'auth/send_request.html', context={"user": Profile.objects.get(pk=pk).user})


class ConfirmAddToFriendsList(View):
    def post(self, request, pk):
        friend_request = FriendRequest.objects.get(pk=pk)
        profile = Profile.objects.get(user=request.user.id)
        profile.friends.add(friend_request.from_user)
        from_profile = Profile.objects.get(user=friend_request.from_user.id)
        from_profile.friends.add(profile.user)
        friend_request.delete()
        success_url = reverse_lazy('auth_app:current_user')
        return HttpResponseRedirect(success_url)

    def get(self, request, pk):
        friend_request = FriendRequest.objects.get(pk=pk)
        return render(request, 'auth/confirm_add_to_friends.html',
                      {"friend_request": friend_request})


class FriendsRequestsView(View):
    def get(self, request):
        friends_requests = FriendRequest.objects.filter(to_user=request.user)
        return render(request, 'auth/friends_requests.html', {"friends_requests": friends_requests})


class DeleteFriendView(View):
    def get(self, request, pk):
        friend = Profile.objects.get(pk=pk)
        return render(request, 'auth/delete_friend.html', {"friend": friend})

    def post(self, request, pk):
        profile = Profile.objects.get(user=request.user.id)
        profile_from = Profile.objects.get(pk=pk)
        profile.friends.remove(Profile.objects.get(pk=pk).user)
        profile_from.friends.remove(profile.user)
        profile.save()
        profile_from.save()
        success_url = reverse('auth_app:current_user')
        return HttpResponseRedirect(success_url)


class UpdateAvatarView(View):
    def post(self, request: HttpRequest):
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            avatar = request.FILES['avatar']
            profile = Profile.objects.get(user=request.user.id)
            profile.avatar = avatar
            profile.save()
            success_url = reverse_lazy("auth_app:current_user")
            return HttpResponseRedirect(success_url)
        return HttpResponseRedirect('/auth/user/change/avatar')

    def get(self, request):
        form = AvatarForm()
        return render(request, 'auth/change_avatar.html', {"form": form})


class UpdateProfileDataView(View):
    def post(self, request):
        form = UpdateProfileInfoForm(request.POST)
        profile = Profile.objects.get(user=request.user.pk)
        if form.is_valid():
            form.change_profile_data(profile=profile)
            success_url = reverse_lazy('auth_app:current_user')
            return HttpResponseRedirect(success_url)

    def get(self, request):
        form = UpdateProfileInfoForm()
        return render(request, 'auth/change_data.html', {"form": form})
