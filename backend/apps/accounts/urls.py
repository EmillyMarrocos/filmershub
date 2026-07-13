# ===========================================
# FILMERSHUB - URLS DE USUÁRIO
# ===========================================

from django.urls import path
from . import views

urlpatterns = [
    # Perfil do usuário logado
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('profile/delete/', views.ProfileDeleteView.as_view(), name='profile-delete'),

    # Perfil público
    path('users/lookup/', views.UserLookupView.as_view(), name='user-lookup'),
    path('users/<uuid:id>/', views.PublicProfileView.as_view(), name='public-profile'),

    # Videomakers
    path('videomakers/', views.VideomakerListView.as_view(), name='videomaker-list'),
    path('videomaker-profile/', views.VideomakerProfileView.as_view(), name='videomaker-profile'),

    # Clientes
    path('client-profile/', views.ClientProfileView.as_view(), name='client-profile'),

    # Seguidores
    path('users/<uuid:id>/follow/', views.FollowToggleView.as_view(), name='follow-toggle'),
    path('users/<uuid:id>/followers/', views.FollowersListView.as_view(), name='followers-list'),
    path('users/<uuid:id>/following/', views.FollowingListView.as_view(), name='following-list'),

    # Habilidades
    path('skills/', views.SkillListView.as_view(), name='skill-list'),
]
