# ===========================================
# FILMERSHUB - CONTRACTS VIEWS
# ===========================================

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from .models import Contract, ContractClause
from .serializers import (
    ContractListSerializer,
    ContractDetailSerializer,
    ContractCreateSerializer,
    ContractClauseCreateSerializer,
)
from .utils import generate_contract_pdf, generate_contract_html


class ContractListView(generics.ListAPIView):
    """GET /api/v1/contracts/"""
    serializer_class = ContractListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Contract.objects.filter(client=user) | Contract.objects.filter(videomaker=user)


class ContractDetailView(generics.RetrieveAPIView):
    """GET /api/v1/contracts/<uuid:pk>/"""
    serializer_class = ContractDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Contract.objects.filter(client=user) | Contract.objects.filter(videomaker=user)


class ContractCreateView(generics.CreateAPIView):
    """POST /api/v1/contracts/"""
    serializer_class = ContractCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        contract = serializer.save(videomaker=self.request.user)
        try:
            pdf_content = generate_contract_pdf(contract)
            contract.pdf_file = pdf_content
            contract.save(update_fields=['pdf_file'])
        except Exception:
            pass


class ContractSignView(APIView):
    """POST /api/v1/contracts/<uuid:pk>/sign/"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        contract = get_object_or_404(Contract, id=pk)

        if request.user not in [contract.client, contract.videomaker]:
            return Response(
                {'detail': 'Você não é parte deste contrato.'},
                status=status.HTTP_403_FORBIDDEN
            )

        if request.user == contract.client and contract.client_signed:
            return Response(
                {'detail': 'Você já assinou este contrato.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.user == contract.videomaker and contract.videomaker_signed:
            return Response(
                {'detail': 'Você já assinou este contrato.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.user == contract.client:
            contract.client_signed = True
            contract.client_signed_at = timezone.now()
        else:
            contract.videomaker_signed = True
            contract.videomaker_signed_at = timezone.now()

        if contract.client_signed and contract.videomaker_signed:
            contract.status = 'signed'

        contract.save()

        try:
            pdf_content = generate_contract_pdf(contract)
            contract.pdf_file = pdf_content
            contract.save(update_fields=['pdf_file'])
        except Exception:
            pass

        return Response(
            {'detail': 'Contrato assinado com sucesso!'},
            status=status.HTTP_200_OK
        )


class ContractPDFView(APIView):
    """GET /api/v1/contracts/<uuid:pk>/pdf/"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        contract = get_object_or_404(Contract, id=pk)

        if request.user not in [contract.client, contract.videomaker]:
            return Response(
                {'detail': 'Você não é parte deste contrato.'},
                status=status.HTTP_403_FORBIDDEN
            )

        if contract.pdf_file:
            response = HttpResponse(contract.pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{contract.contract_number}.pdf"'
            return response

        html_content = generate_contract_html(contract)
        try:
            from weasyprint import HTML
            pdf_bytes = HTML(string=html_content).write_pdf()
            response = HttpResponse(pdf_bytes, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{contract.contract_number}.pdf"'
            return response
        except Exception:
            return Response(
                {'detail': 'Erro ao gerar PDF.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ContractClauseCreateView(generics.CreateAPIView):
    """POST /api/v1/contracts/<uuid:contract_id>/clauses/"""
    serializer_class = ContractClauseCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        contract = get_object_or_404(
            Contract.objects.filter(videomaker=self.request.user),
            id=self.kwargs['contract_id']
        )
        serializer.save(contract=contract)
