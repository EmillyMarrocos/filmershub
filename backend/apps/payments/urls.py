from django.urls import path
from . import views

urlpatterns = [
    path('', views.PaymentListView.as_view(), name='payment-list'),
    path('<uuid:pk>/', views.PaymentDetailView.as_view(), name='payment-detail'),
    path('create/', views.PaymentCreateView.as_view(), name='payment-create'),
    path('webhook/', views.PaymentWebhookView.as_view(), name='payment-webhook'),
    path('<uuid:payment_id>/refund/', views.RefundCreateView.as_view(), name='refund-create'),
]
