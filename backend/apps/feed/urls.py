from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='post-list'),
    path('create/', views.PostCreateView.as_view(), name='post-create'),
    path('<uuid:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('<uuid:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('<uuid:post_id>/like/', views.LikeToggleView.as_view(), name='like-toggle'),
    path('<uuid:post_id>/comments/', views.CommentListView.as_view(), name='comment-list'),
    path('<uuid:post_id>/comments/create/', views.CommentCreateView.as_view(), name='comment-create'),
]
