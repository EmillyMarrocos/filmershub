# ===========================================
# FILMERSHUB - PAYMENTS VIEWS
# ===========================================

import mercadopago
from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Payment, Refund
from apps.contracts.models import Contract
from .serializers import (
    PaymentListSerializer,
    PaymentDetailSerializer,
    PaymentCreateSerializer,
    RefundCreateSerializer,
)


class PaymentListView(generics.ListAPIView):
    """GET /api/v1/payments/"""
    serializer_class = PaymentListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Payment.objects.filter(payer=user) | Payment.objects.filter(payee=user)


class PaymentDetailView(generics.RetrieveAPIView):
    """GET /api/v1/payments/<uuid:pk>/"""
    serializer_class = PaymentDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Payment.objects.filter(payer=user) | Payment.objects.filter(payee=user)


class PaymentCreateView(APIView):
    """POST /api/v1/payments/create/"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PaymentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        contract = get_object_or_404(Contract, id=serializer.validated_data['contract_id'])

        # Verifica se o usuário é o pagador
        if request.user != contract.client:
            return Response(
                {'detail': 'Apenas o cliente pode criar pagamentos.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Cria pagamento no banco
        payment = Payment.objects.create(
            contract=contract,
            payer=contract.client,
            payee=contract.videomaker,
            total_amount=contract.total_value,
            payment_method=serializer.validated_data['payment_method'],
            status='pending',
        )

        # Integração com Mercado Pago
        try:
            sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)

            preference_data = {
                "items": [
                    {
                        "id": str(contract.contract_number),
                        "title": f"FilmersHub - {contract.service_type}",
                        "quantity": 1,
                        "unit_price": float(contract.total_value),
                    }
                ],
                "payment_methods": {
                    "excluded_payment_types": [],
                    "installments": serializer.validated_data.get('installments', 1)
                },
                "metadata": {
                    "contract_id": str(contract.id),
                    "payment_id": str(payment.id),
                }
            }

            preference_response = sdk.preference().create(preference_data)
            preference = preference_response["response"]

            payment.mp_preference_id = preference.get("id", "")
            payment.save(update_fields=['mp_preference_id'])

            return Response({
                'detail': 'Pagamento criado com sucesso!',
                'payment_id': str(payment.id),
                'init_point': preference.get("init_point", ""),
                'sandbox_init_point': preference.get("sandbox_init_point", ""),
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            payment.status = 'rejected'
            payment.notes = str(e)
            payment.save()

            return Response(
                {'detail': f'Erro ao criar pagamento: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PaymentWebhookView(APIView):
    """POST /api/v1/payments/webhook/"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Webhook do Mercado Pago para notificações de pagamento."""
        data = request.data

        if data.get('type') == 'payment':
            payment_id = data.get('data', {}).get('id')

            try:
                sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)
                payment_response = sdk.payment().get(payment_id)
                payment_data = payment_response["response"]

                # Busca o pagamento no banco
                mp_payment_id = str(payment_data.get('id'))
                payment = Payment.objects.filter(mp_payment_id=mp_payment_id).first()

                if payment:
                    payment_status = payment_data.get('status')
                    if payment_status == 'approved':
                        payment.status = 'approved'
                        payment.paid_at = payment_data.get('date_approved')
                    elif payment_status == 'rejected':
                        payment.status = 'rejected'
                    elif payment_status == 'refunded':
                        payment.status = 'refunded'

                    payment.mp_transaction_id = payment_data.get('transaction_id', '')
                    payment.save()

            except Exception as e:
                pass  # Log erro mas retorna 200 para o MP

        return Response(status=status.HTTP_200_OK)


class RefundCreateView(APIView):
    """POST /api/v1/payments/<uuid:payment_id>/refund/"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, payment_id):
        payment = get_object_or_404(Payment, id=payment_id, payee=request.user)

        serializer = RefundCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']

        if amount > payment.total_amount:
            return Response(
                {'detail': 'Valor do reembolso excede o pagamento.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        refund = Refund.objects.create(
            payment=payment,
            amount=amount,
            reason=serializer.validated_data['reason'],
            status='processing'
        )

        # Integração com Mercado Pago
        try:
            sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)
            refund_response = sdk.payment().refund(payment.mp_payment_id, {
                "amount": float(amount)
            })

            refund.mp_refund_id = str(refund_response["response"].get("id", ""))
            refund.status = 'approved'
            refund.save()

        except Exception as e:
            refund.status = 'rejected'
            refund.save()

        return Response(
            {'detail': 'Reembolso processado.', 'refund_id': str(refund.id)},
            status=status.HTTP_200_OK
        )
