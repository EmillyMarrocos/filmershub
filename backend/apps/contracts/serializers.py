# ===========================================
# FILMERSHUB - CONTRACTS SERIALIZERS
# ===========================================

from rest_framework import serializers
from .models import Contract, ContractClause


class ContractClauseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractClause
        fields = ['id', 'clause_type', 'title', 'content', 'order']


class ContractListSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.full_name', read_only=True)
    videomaker_name = serializers.CharField(source='videomaker.full_name', read_only=True)

    class Meta:
        model = Contract
        fields = [
            'id', 'contract_number', 'client', 'client_name',
            'videomaker', 'videomaker_name', 'service_type',
            'total_value', 'status', 'client_signed', 'videomaker_signed',
            'created_at',
        ]


class ContractDetailSerializer(ContractListSerializer):
    clauses = ContractClauseSerializer(many=True, read_only=True)

    class Meta(ContractListSerializer.Meta):
        fields = ContractListSerializer.Meta.fields + [
            'service_description', 'event_date', 'delivery_date',
            'location', 'payment_method', 'pdf_file', 'content_hash',
            'client_signed_at', 'videomaker_signed_at',
            'additional_clauses', 'clauses', 'updated_at',
        ]


class ContractCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = [
            'client', 'service_type', 'service_description',
            'event_date', 'delivery_date', 'location',
            'total_value', 'payment_method', 'additional_clauses',
        ]

    def validate(self, attrs):
        if attrs['client'] == self.context['request'].user:
            raise serializers.ValidationError('Não pode criar contrato consigo mesmo.')
        if attrs['event_date'] >= attrs['delivery_date']:
            raise serializers.ValidationError('Data de entrega deve ser após data do evento.')
        return attrs


class ContractClauseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractClause
        fields = ['clause_type', 'title', 'content', 'order']
