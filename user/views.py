from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View

from .models import Profile
from .forms import EditProfileForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


# Create your views here.
    
def DetailProfile(request, username):
    user = get_user_model().objects.filter(username=username).first()
    profile = Profile.objects.get(user=user)

    try:
        is_following = request.user.followers.get(user=user)
    except:
        is_following = None

    context={
        'user':user,
        'profile':profile,
        'is_following':is_following,
    }

    return render(request, 'users/detail.html', context)

@login_required
def EditProfile(request):
    context = {}
    
    User = get_user_model()
    user = request.user.id
    profile = Profile.objects.get(user__id=user)
    user_basic_info = User.objects.get(id=user)

    if request.POST:
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            user_basic_info.first_name = form.cleaned_data.get('first_name')
            user_basic_info.last_name = form.cleaned_data.get('last_name')

            profile.picture = form.cleaned_data.get('picture')
            profile.banner = form.cleaned_data.get('banner')
            profile.location = form.cleaned_data.get('location')
            profile.url = form.cleaned_data.get('url')
            profile.bio = form.cleaned_data.get('bio')
            profile.birthday = form.cleaned_data.get('birthday')

            profile.save()
            user_basic_info.save()
            return redirect('user:profile', username=request.user.username)
        else:
            context['errors'] = list(map(lambda x: x, list(form.errors.values())))
    else:
        form = EditProfileForm(instance=profile)

    context['form'] = form
    return render(request, 'users/edit.html', context)
    
class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        profile.followers.add(request.user)

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'User Followed'
        )

        return redirect('user:profile', username=profile.user.username)
    
class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        profile.followers.remove(request.user)
        
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'User Unfollowed'
        )

        return redirect('user:profile', username=profile.user.username)
    
class ListFollowers(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        followers = profile.followers.all()

        context = {
            'profile': profile,
            'followers': followers
        }

        return render(request, 'social/pages/followers_list.html', context)