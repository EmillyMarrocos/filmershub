# ===========================================
# FILMERSHUB - PAYMENTS SERIALIZERS
# ===========================================

from rest_framework import serializers
from .models import Payment, Refund


class PaymentListSerializer(serializers.ModelSerializer):
    contract_number = serializers.CharField(source='contract.contract_number', read_only=True)
    payer_name = serializers.CharField(source='payer.full_name', read_only=True)
    payee_name = serializers.CharField(source='payee.full_name', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'contract', 'contract_number',
            'payer', 'payer_name', 'payee', 'payee_name',
            'total_amount', 'payment_method', 'status',
            'paid_at', 'created_at',
        ]


class PaymentDetailSerializer(PaymentListSerializer):
    class Meta(PaymentListSerializer.Meta):
        fields = PaymentListSerializer.Meta.fields + [
            'platform_fee', 'videomaker_amount',
            'mp_payment_id', 'card_last_four', 'notes',
        ]


class PaymentCreateSerializer(serializers.Serializer):
    """Serializer para criar pagamento via Mercado Pago."""
    contract_id = serializers.UUIDField()
    payment_method = serializers.ChoiceField(choices=['pix', 'credit_card'])
    token = serializers.CharField(required=False, allow_blank=True)
    installments = serializers.IntegerField(default=1)


class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = [
            'id', 'payment', 'amount', 'reason',
            'status', 'mp_refund_id', 'processed_at', 'created_at',
        ]
        read_only_fields = ['status', 'mp_refund_id', 'processed_at']


class RefundCreateSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    reason = serializers.CharField()
