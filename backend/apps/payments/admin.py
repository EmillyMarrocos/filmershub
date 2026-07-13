from django.contrib import admin
from .models import Payment, Refund


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'contract', 'payer', 'payee', 'total_amount',
        'payment_method', 'status', 'paid_at', 'created_at'
    )
    list_filter = ('status', 'payment_method')
    search_fields = ('contract__contract_number', 'payer__email')
    raw_id_fields = ('contract', 'payer', 'payee')
    readonly_fields = ('mp_payment_id', 'mp_preference_id', 'mp_transaction_id')


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('payment', 'amount', 'reason', 'status', 'created_at')
    list_filter = ('status',)
    raw_id_fields = ('payment',)
