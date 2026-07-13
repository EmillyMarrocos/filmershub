from django.urls import path
from . import views

urlpatterns = [
    path('availability/', views.AvailabilityListView.as_view(), name='availability-list'),
    path('availability/create/', views.AvailabilityCreateView.as_view(), name='availability-create'),
    path('events/', views.EventListView.as_view(), name='event-list'),
    path('events/create/', views.EventCreateView.as_view(), name='event-create'),
    path('events/<uuid:pk>/', views.EventDetailView.as_view(), name='event-detail'),
    path('booking-requests/', views.BookingRequestListView.as_view(), name='booking-list'),
    path('booking-requests/create/', views.BookingRequestCreateView.as_view(), name='booking-create'),
    path('booking-requests/<uuid:pk>/respond/', views.BookingRequestResponseView.as_view(), name='booking-respond'),
]
