from django.urls import path
from . import views
from .feeds import LatestPostFeed
# app_name = 'blog' 
urlpatterns = [
    path('', views.post_list, name='post_lists'),
    path('tag/<slug:tag_slug>', views.post_list, name='post_lists_tag'),
    path('detail/<int:year>/<int:month>/<int:day>/<slug:slug_info>/', views.post_detail, name='post_detail'),
    path('share/<int:pk>', views.post_share, name ='post_share'),
    path('comment/<int:pk>', views.post_comment, name='post_comment'),
    path('feed/', LatestPostFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
]
