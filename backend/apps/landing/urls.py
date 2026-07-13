from django.urls import path
from . import views

urlpatterns = [
    path('stats/', views.LandingStatsView.as_view(), name='landing-stats'),
    path('featured-videomakers/', views.FeaturedVideomakersView.as_view(), name='featured-videomakers'),
    path('featured-works/', views.FeaturedWorksView.as_view(), name='featured-works'),
]
