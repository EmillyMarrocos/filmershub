from django.contrib import admin
from .models import Contract, ContractClause


class ContractClauseInline(admin.TabularInline):
    model = ContractClause
    extra = 0
    ordering = ['order']


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = (
        'contract_number', 'client', 'videomaker',
        'service_type', 'total_value', 'status',
        'client_signed', 'videomaker_signed', 'created_at'
    )
    list_filter = ('status', 'service_type', 'payment_method')
    search_fields = ('contract_number', 'client__email', 'videomaker__email')
    raw_id_fields = ('client', 'videomaker')
    inlines = [ContractClauseInline]
    readonly_fields = ('contract_number', 'content_hash')


@admin.register(ContractClause)
class ContractClauseAdmin(admin.ModelAdmin):
    list_display = ('contract', 'clause_type', 'title', 'order')
    list_filter = ('clause_type',)
    raw_id_fields = ('contract',)
