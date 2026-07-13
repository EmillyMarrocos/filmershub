from django.urls import path
from . import views

urlpatterns = [
    path('', views.ContractListView.as_view(), name='contract-list'),
    path('create/', views.ContractCreateView.as_view(), name='contract-create'),
    path('<uuid:pk>/', views.ContractDetailView.as_view(), name='contract-detail'),
    path('<uuid:pk>/sign/', views.ContractSignView.as_view(), name='contract-sign'),
    path('<uuid:contract_id>/clauses/', views.ContractClauseCreateView.as_view(), name='clause-create'),
]
