from . import views
from django.urls import path

from .views import ReadLaterView

urlpatterns = [

    path('', views.StartingPage.as_view(), name='starting_page'),
    path('posts/', views.AllPostsView.as_view(), name='posts'),
    path('posts/<slug:slug>/', views.SignalPostView.as_view(),
         name='post_info'),
    path('read-later', ReadLaterView.as_view(), name='read_later'),
]