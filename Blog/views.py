from django.shortcuts import render
from .models import *
def starting_page(request):
    posts_info = Post.objects.all().order_by("date")
    print(posts_info[0].date)
    return render(request, 'Blog/starting_page.html',{'post_info': posts_info})

def posts(request):
    all_posts = Post.objects.all().order_by("date")
    return render(request, 'Blog/all-posts.html', {'all_posts': all_posts})

def post_info(request, slug):
    ind = Post.objects.get(slug=slug)
    return render(request, 'Blog/post_info.html',{'post': ind})