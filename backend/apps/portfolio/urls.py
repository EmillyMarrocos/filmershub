from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('works/', views.WorkListView.as_view(), name='work-list'),
    path('works/<uuid:pk>/', views.WorkDetailView.as_view(), name='work-detail'),
    path('works/mine/', views.WorkUpdateView.as_view(), name='work-mine'),
    path('reviews/', views.ReviewListCreateView.as_view(), name='review-list-create'),
]
