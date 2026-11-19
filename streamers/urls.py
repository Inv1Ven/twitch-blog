from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = 'streamers'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('tag/<str:tag_slug>/', views.PostListView.as_view(), name='post_list_by_tag'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<int:pk>/like/', views.like_post, name='like_post'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('rss/feed/', LatestPostsFeed(), name='latest_feed'),
]