# ===========================================
# FILMERSHUB - SCHEDULING SERIALIZERS
# ===========================================

from rest_framework import serializers
from .models import Availability, Event, BookingRequest


class AvailabilitySerializer(serializers.ModelSerializer):
    day_name = serializers.CharField(source='get_day_of_week_display', read_only=True)

    class Meta:
        model = Availability
        fields = ['id', 'day_of_week', 'day_name', 'start_time', 'end_time', 'is_available']


class EventListSerializer(serializers.ModelSerializer):
    videomaker_name = serializers.CharField(source='videomaker.full_name', read_only=True)
    client_name = serializers.CharField(source='client.full_name', read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'event_type', 'videomaker', 'videomaker_name',
            'client', 'client_name', 'start_datetime', 'end_datetime',
            'location', 'status', 'total_price',
        ]


class EventDetailSerializer(EventListSerializer):
    class Meta(EventListSerializer.Meta):
        fields = EventListSerializer.Meta.fields + [
            'description', 'address', 'notes', 'created_at',
        ]


class EventCreateSerializer(serializers.ModelSerializer):
    client_email = serializers.EmailField(required=False, write_only=True)

    class Meta:
        model = Event
        fields = [
            'title', 'description', 'event_type',
            'start_datetime', 'end_datetime', 'location',
            'address', 'total_price', 'notes', 'client_email',
        ]

    def validate(self, attrs):
        start = attrs.get('start_datetime')
        end = attrs.get('end_datetime')
        if start and end and start >= end:
            raise serializers.ValidationError('Data fim deve ser após data início.')
        return attrs


class BookingRequestListSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.full_name', read_only=True)
    videomaker_name = serializers.CharField(source='videomaker.full_name', read_only=True)

    class Meta:
        model = BookingRequest
        fields = [
            'id', 'client', 'client_name', 'videomaker', 'videomaker_name',
            'event_type', 'preferred_date', 'preferred_time',
            'status', 'created_at',
        ]


class BookingRequestDetailSerializer(BookingRequestListSerializer):
    class Meta(BookingRequestListSerializer.Meta):
        fields = BookingRequestListSerializer.Meta.fields + [
            'description', 'estimated_duration', 'location', 'budget',
            'decline_reason', 'responded_at',
        ]


class BookingRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingRequest
        fields = [
            'videomaker', 'event_type', 'description',
            'preferred_date', 'preferred_time', 'estimated_duration',
            'location', 'budget',
        ]

    def validate(self, attrs):
        if attrs['videomaker'] == self.context['request'].user:
            raise serializers.ValidationError('Não pode agendar consigo mesmo.')
        return attrs


class BookingRequestResponseSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['accept', 'decline'])
    decline_reason = serializers.CharField(required=False, allow_blank=True)
