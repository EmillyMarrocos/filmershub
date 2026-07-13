# ===========================================
# FILMERSHUB - SCHEDULING VIEWS
# ===========================================

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Availability, Event, BookingRequest
from .serializers import (
    AvailabilitySerializer,
    EventListSerializer,
    EventDetailSerializer,
    EventCreateSerializer,
    BookingRequestListSerializer,
    BookingRequestDetailSerializer,
    BookingRequestCreateSerializer,
    BookingRequestResponseSerializer,
)


class AvailabilityListView(generics.ListAPIView):
    """GET /api/v1/scheduling/availability/?videomaker=<uuid>"""
    serializer_class = AvailabilitySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        videomaker_id = self.request.query_params.get('videomaker')
        if videomaker_id:
            return Availability.objects.filter(videomaker_id=videomaker_id)
        return Availability.objects.filter(videomaker=self.request.user)


class AvailabilityCreateView(generics.CreateAPIView):
    """POST /api/v1/scheduling/availability/"""
    serializer_class = AvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(videomaker=self.request.user)


class EventListView(generics.ListAPIView):
    """GET /api/v1/scheduling/events/"""
    serializer_class = EventListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Event.objects.filter(
            videomaker=user
        ) | Event.objects.filter(client=user)


class EventDetailView(generics.RetrieveAPIView):
    """GET /api/v1/scheduling/events/<uuid:pk>/"""
    serializer_class = EventDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Event.objects.filter(videomaker=user) | Event.objects.filter(client=user)


class EventCreateView(generics.CreateAPIView):
    """POST /api/v1/scheduling/events/"""
    serializer_class = EventCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        client_email = serializer.validated_data.pop('client_email', None)
        client = self.request.user
        if client_email:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            found = User.objects.filter(email__iexact=client_email, is_active=True).first()
            if found:
                client = found
        serializer.save(videomaker=self.request.user, client=client)


class BookingRequestListView(generics.ListAPIView):
    """GET /api/v1/scheduling/booking-requests/"""
    serializer_class = BookingRequestListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return BookingRequest.objects.filter(client=user) | BookingRequest.objects.filter(videomaker=user)


class BookingRequestCreateView(generics.CreateAPIView):
    """POST /api/v1/scheduling/booking-requests/"""
    serializer_class = BookingRequestCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


class BookingRequestResponseView(APIView):
    """POST /api/v1/scheduling/booking-requests/<uuid:pk>/respond/"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        booking = get_object_or_404(
            BookingRequest.objects.filter(videomaker=request.user),
            id=pk,
            status='pending'
        )

        serializer = BookingRequestResponseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action = serializer.validated_data['action']

        if action == 'accept':
            booking.status = 'accepted'
        else:
            booking.status = 'declined'
            booking.decline_reason = serializer.validated_data.get('decline_reason', '')

        booking.responded_at = timezone.now()
        booking.save()

        return Response(
            {'detail': f'Solicitação {booking.get_status_display()}.'},
            status=status.HTTP_200_OK
        )
