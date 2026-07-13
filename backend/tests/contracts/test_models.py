# ===========================================
# FILMERSHUB - TESTES DE MODELOS (CONTRACTS)
# ===========================================

import pytest
from django.contrib.auth import get_user_model
from apps.contracts.models import Contract, ContractClause

User = get_user_model()


@pytest.mark.django_db
class TestContract:
    """Testes para o modelo Contract."""

    def test_create_contract(self, user, videomaker_user):
        """Testa criação de contrato."""
        contract = Contract.objects.create(
            client=user,
            videomaker=videomaker_user,
            service_type='wedding',
            service_description='Filmagem de casamento',
            event_date='2026-12-25',
            delivery_date='2027-01-15',
            location='São Paulo, SP',
            total_value=3500.00,
            payment_method='pix',
        )
        assert contract.client == user
        assert contract.videomaker == videomaker_user
        assert contract.total_value == 3500.00

    def test_contract_number_generation(self, user, videomaker_user):
        """Testa geração automática do número do contrato."""
        contract = Contract.objects.create(
            client=user,
            videomaker=videomaker_user,
            service_type='corporate',
            service_description='Vídeo institucional',
            event_date='2026-12-20',
            delivery_date='2027-01-10',
            location='Rio de Janeiro, RJ',
            total_value=5000.00,
        )
        assert contract.contract_number.startswith('FH-')
        assert len(contract.contract_number) == 13  # FH-2026-00001

    def test_contract_hash_generation(self, user, videomaker_user):
        """Testa geração automática do hash SHA-256."""
        contract = Contract.objects.create(
            client=user,
            videomaker=videomaker_user,
            service_type='event',
            service_description='Evento corporativo',
            event_date='2026-12-18',
            delivery_date='2027-01-05',
            location='Belo Horizonte, MG',
            total_value=2500.00,
        )
        assert len(contract.content_hash) == 64  # SHA-256

    def test_contract_str(self, user, videomaker_user):
        """Testa representação string."""
        contract = Contract(
            contract_number='FH-2026-00001',
            client=user,
            videomaker=videomaker_user,
        )
        assert str(contract) == 'FH-2026-00001 - Test User ↔ John Doe'

    def test_contract_signatures(self, user, videomaker_user):
        """Testa assinaturas do contrato."""
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
        assert contract.client_signed is False
        assert contract.videomaker_signed is False


@pytest.mark.django_db
class TestContractClause:
    """Testes para o modelo ContractClause."""

    def test_create_clause(self, user, videomaker_user):
        """Testa criação de cláusula."""
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
        clause = ContractClause.objects.create(
            contract=contract,
            clause_type='payment',
            title='Condições de Pagamento',
            content='Pagamento antecipado de 50%.',
            order=1,
        )
        assert clause.contract == contract
        assert clause.clause_type == 'payment'

    def test_clause_str(self, user, videomaker_user):
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
        clause = ContractClause(
            contract=contract,
            title='Cláusula de Sigilo',
        )
        assert str(clause) == 'FH-2026-00001 - Cláusula de Sigilo'
