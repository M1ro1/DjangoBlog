from . import views
from django.urls import path
urlpatterns = [

    path('', views.starting_page, name='starting_page'),
    path('posts/', views.posts, name='posts'),
    path('posts/<slug:slug>/', views.post_info, name='post_info'),
]