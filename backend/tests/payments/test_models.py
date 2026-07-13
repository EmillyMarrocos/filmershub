# ===========================================
# FILMERSHUB - TESTES DE MODELOS (PAYMENTS)
# ===========================================

import pytest
from django.contrib.auth import get_user_model
from apps.contracts.models import Contract
from apps.payments.models import Payment, Refund

User = get_user_model()


@pytest.mark.django_db
class TestPayment:
    """Testes para o modelo Payment."""

    def test_create_payment(self, user, videomaker_user):
        """Testa criação de pagamento."""
        contract = Contract.objects.create(
            client=user,
            videomaker=videomaker_user,
            service_type='wedding',
            service_description='Filmagem',
            event_date='2026-12-25',
            delivery_date='2027-01-15',
            location='SP',
            total_value=3000.00,
        )
        payment = Payment.objects.create(
            contract=contract,
            payer=user,
            payee=videomaker_user,
            total_amount=3000.00,
            payment_method='pix',
        )
        assert payment.total_amount == 3000.00
        assert payment.status == 'pending'

    def test_payment_split_calculation(self, user, videomaker_user):
        """Testa cálculo automático do split."""
        contract = Contract.objects.create(
            client=user,
            videomaker=videomaker_user,
            service_type='corporate',
            service_description='Vídeo',
            event_date='2026-12-20',
            delivery_date='2027-01-10',
            location='RJ',
            total_value=5000.00,
        )
        payment = Payment.objects.create(
            contract=contract,
            payer=user,
            payee=videomaker_user,
            total_amount=5000.00,
        )
        # 15% plataforma = 750, 85% videomaker = 4250
        assert payment.platform_fee == 750.00
        assert payment.videomaker_amount == 4250.00

    def test_payment_str(self, user, videomaker_user):
        """Testa representação string."""
        contract = Contract.objects.create(
            client=user,
            videomaker=videomaker_user,
            service_type='wedding',
            service_description='Filmagem',
            event_date='2026-12-25',
            delivery_date='2027-01-15',
            location='SP',
            total_value=3000.00,
            contract_number='FH-2026-00001',
        )
        payment = Payment(
            contract=contract,
            total_amount=3000.00,
        )
        assert '3000' in str(payment)


@pytest.mark.django_db
class TestRefund:
    """Testes para o modelo Refund."""

    def test_create_refund(self, user, videomaker_user):
        """Testa criação de reembolso."""
        contract = Contract.objects.create(
            client=user,
            videomaker=videomaker_user,
            service_type='wedding',
            service_description='Filmagem',
            event_date='2026-12-25',
            delivery_date='2027-01-15',
            location='SP',
            total_value=3000.00,
        )
        payment = Payment.objects.create(
            contract=contract,
            payer=user,
            payee=videomaker_user,
            total_amount=3000.00,
            status='approved',
        )
        refund = Refund.objects.create(
            payment=payment,
            amount=1500.00,
            reason='Evento cancelado',
        )
        assert refund.amount == 1500.00
        assert refund.status == 'pending'

    def test_refund_str(self, user, videomaker_user):
        """Testa representação string."""
        contract = Contract.objects.create(
            client=user,
            videomaker=videomaker_user,
            service_type='wedding',
            service_description='Filmagem',
            event_date='2026-12-25',
            delivery_date='2027-01-15',
            location='SP',
            total_value=3000.00,
        )
        payment = Payment.objects.create(
            contract=contract,
            payer=user,
            payee=videomaker_user,
            total_amount=3000.00,
        )
        refund = Refund(
            payment=payment,
            amount=500.00,
        )
        assert '500' in str(refund)
