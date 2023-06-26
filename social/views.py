from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.urls.base import reverse_lazy
from django.http import HttpResponseRedirect

from .models import SocialPost, SocialComment
from .forms import SocialCommentForm

class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = SocialPost.objects.get(pk=pk)

        is_dislike = list(filter(lambda dislike: dislike == request.user, post.dislikes.all()))
        is_like = list(filter(lambda like: like == request.user, post.likes.all()))

        comments = SocialComment.objects.filter(post=post).order_by('-created_on')

        form = SocialCommentForm()

        context = {
            'post': post,
            'is_dislike': is_dislike,
            'is_like': is_like,
            'form': form,
            'comments': comments
        }
        return render(request, 'pages/social/detail.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        post = SocialPost.objects.get(pk=pk)

        form = SocialCommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            
        return HttpResponseRedirect(self.request.path_info)

class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SocialPost
    fields = ['body']
    template_name = 'pages/social/edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('social:post-detail', kwargs={'pk':pk})
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = SocialPost
    template_name = 'pages/social/delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk,*args, **kwargs):
        post = SocialPost.objects.get(pk=pk)

        is_dislike = list(filter(lambda dislike: dislike == request.user, post.dislikes.all()))

        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = list(filter(lambda like: like == request.user, post.likes.all()))

        if not is_like:
            post.likes.add(request.user)
        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
    
class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk,*args, **kwargs):
        post = SocialPost.objects.get(pk=pk)

        is_like = list(filter(lambda like: like == request.user, post.likes.all()))

        if is_like:
            post.likes.remove(request.user)

        is_dislike = list(filter(lambda dislike: dislike == request.user, post.dislikes.all()))

        if not is_dislike:
            post.dislikes.add(request.user)
        if is_dislike:
            post.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
    
class CommentLike(LoginRequiredMixin, View):
    def post(self, request, pk,*args, **kwargs):
        comment = SocialComment.objects.get(pk=pk)

        is_dislike = list(filter(lambda dislike: dislike == request.user, comment.dislikes.all()))

        if is_dislike:
            comment.dislikes.remove(request.user)

        is_like = list(filter(lambda like: like == request.user, comment.likes.all()))

        if not is_like:
            comment.likes.add(request.user)
        if is_like:
            comment.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
    
class CommentDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = SocialComment.objects.get(pk=pk)

        is_like = list(filter(lambda like: like == request.user, comment.likes.all()))

        if is_like:
            comment.likes.remove(request.user)

        is_dislike = list(filter(lambda dislike: dislike == request.user, comment.dislikes.all()))

        if not is_dislike:
            comment.dislikes.add(request.user)
        if is_dislike:
            comment.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
    
class CommentReply(LoginRequiredMixin, View):
    def post(self, request, pk, post_pk, *args, **kwargs):
        post = SocialPost.objects.get(pk=post_pk)
        parent_comment = SocialComment.objects.get(pk=pk)
        form = SocialCommentForm(request.POST)
        
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.parent = parent_comment
            new_comment.save()

        return redirect('social:post-detail', pk=post.pk)

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = SocialComment
    template_name = 'pages/social/comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('social:post-detail', kwargs={'pk':pk})
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

class CommentEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SocialComment
    fields = ['comment']
    template_name = 'pages/social/comment_edit.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('social:post-detail', kwargs={'pk':pk})
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author