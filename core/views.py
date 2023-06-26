from django.views.generic import TemplateView, View
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib import messages

from social.models import Image, SocialPost
from social.forms import SocialPostForm

class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logged_in_user = request.user

        posts = SocialPost.objects.all().order_by('-created_on')

        form = SocialPostForm()

        context = {
            'form': form,
            'posts': posts
        }
        return render(request, 'pages/index.html', context)
    
    def post(self, request, *args, **kwargs):
        logged_in_user = request.user

        posts = SocialPost.objects.all()
        
        form = SocialPostForm(request.POST, request.FILES)
        
        images = request.FILES.getlist('images')

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = logged_in_user
            new_post.save()

            for image in images:
                post_images = Image.objects.create(
                    post = new_post,
                    image = image
                )
        else:
            for error in form.errors.values():
                messages.error(request, error.as_text().strip('*'))
        
        return HttpResponseRedirect(self.request.path_info)