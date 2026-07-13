from django.urls import path
from . import views

urlpatterns = [
    path('rooms/', views.ChatRoomListView.as_view(), name='room-list'),
    path('rooms/create/', views.ChatRoomCreateView.as_view(), name='room-create'),
    path('rooms/<uuid:pk>/', views.ChatRoomDetailView.as_view(), name='room-detail'),
    path('rooms/<uuid:room_id>/messages/', views.MessageListView.as_view(), name='message-list'),
    path('rooms/<uuid:room_id>/messages/send/', views.MessageCreateView.as_view(), name='message-create'),
    path('rooms/<uuid:room_id>/read/', views.MarkMessagesReadView.as_view(), name='messages-read'),
]
