from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import *
from django.views.generic import ListView
from .forms import CommentForm
from django.views import View
from django.urls import reverse

class StartingPage(ListView):
    model = Post
    template_name = 'Blog/starting_page.html'
    ordering = ['-date']
    context_object_name = 'post_info'

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data

class AllPostsView(ListView):
    model = Post
    template_name = 'Blog/all-posts.html'
    ordering = ['-date']
    context_object_name = 'all_posts'

class SignalPostView(View):
    template_name = 'Blog/post_info.html'
    model = Post

    def get(self, request,slug):
        post = Post.objects.get(slug=slug)
        context = {
            'post': post,
            'comment_form': CommentForm(),
            'comments': post.comments.all().order_by('-id'),
        }
        return render(request, 'Blog/post_info.html',
                      context)

    def post(self, request,slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()

            return HttpResponseRedirect(reverse('post_info', args=[slug]))

        context = {
            'post': post,
            'comment_form': comment_form,
            'comments': post.comments.all().order_by('-id'),

        }
        return render(request, 'Blog/post_info.html', context)

class ReadLaterView(View):
    def get(self,request):
        stored_posts = request.session.get('stored_posts')

        context = {}
        if not stored_posts:
            context['posts'] = []
            context['has_posts'] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context['posts'] = posts
            context['has_posts'] = True

        return render(request, 'Blog/stored_posts.html', context)

    def post(self,request):
        stored_posts = request.session.get('stored_posts')

        if stored_posts is None:
            stored_posts = []

        try:
            post_id = int(request.POST.get('post_id'))
        except (TypeError, ValueError):
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        action = request.POST.get('action', 'add')

        if action == 'remove':
            if post_id in stored_posts:
                stored_posts.remove(post_id)
                request.session['stored_posts'] = stored_posts
            return HttpResponseRedirect(reverse('read_later'))

        if post_id not in stored_posts:
            stored_posts.append(post_id)
            request.session['stored_posts'] = stored_posts

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
