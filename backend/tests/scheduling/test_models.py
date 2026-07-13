# ===========================================
# FILMERSHUB - TESTES DE MODELOS (SCHEDULING)
# ===========================================

import pytest
from datetime import timedelta
from django.contrib.auth import get_user_model
from apps.scheduling.models import Availability, Event, BookingRequest

User = get_user_model()


@pytest.mark.django_db
class TestAvailability:
    """Testes para o modelo Availability."""

    def test_create_availability(self, videomaker_user):
        """Testa criação de disponibilidade."""
        avail = Availability.objects.create(
            videomaker=videomaker_user,
            day_of_week=0,  # Segunda
            start_time='09:00',
            end_time='18:00',
        )
        assert avail.day_of_week == 0
        assert avail.is_available is True

    def test_availability_str(self, videomaker_user):
        """Testa representação string."""
        avail = Availability(
            videomaker=videomaker_user,
            day_of_week=0,
        )
        assert 'John Doe' in str(avail)


@pytest.mark.django_db
class TestEvent:
    """Testes para o modelo Event."""

    def test_create_event(self, user, videomaker_user):
        """Testa criação de evento."""
        event = Event.objects.create(
            title='Casamento Silva',
            event_type='wedding',
            videomaker=videomaker_user,
            client=user,
            start_datetime='2026-12-25 14:00:00',
            end_datetime='2026-12-25 22:00:00',
            location='Igreja São Paulo',
            total_price=3500.00,
        )
        assert event.title == 'Casamento Silva'
        assert event.status == 'pending'

    def test_event_str(self, user, videomaker_user):
        """Testa representação string."""
        event = Event(
            title='Evento',
            start_datetime='2026-12-25 14:00:00',
        )
        assert str(event) != ''


@pytest.mark.django_db
class TestBookingRequest:
    """Testes para o modelo BookingRequest."""

    def test_create_booking(self, user, videomaker_user):
        """Testa criação de solicitação."""
        booking = BookingRequest.objects.create(
            client=user,
            videomaker=videomaker_user,
            event_type='wedding',
            description='Preciso de um videografo para meu casamento',
            preferred_date='2026-12-25',
            preferred_time='14:00',
            estimated_duration=timedelta(hours=8),
            budget=3000.00,
        )
        assert booking.status == 'pending'

    def test_booking_str(self, user, videomaker_user):
        """Testa representação string."""
        booking = BookingRequest(
            client=user,
            videomaker=videomaker_user,
        )
        assert 'Test User' in str(booking)
        assert 'John Doe' in str(booking)
