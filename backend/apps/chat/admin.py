from django.contrib import admin
from .models import ChatRoom, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('sender', 'message_type', 'content', 'created_at')


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_type', 'participant_names', 'last_message_preview', 'updated_at')
    list_filter = ('room_type',)
    filter_horizontal = ('participants',)
    inlines = [MessageInline]

    def participant_names(self, obj):
        return ', '.join([p.full_name for p in obj.participants.all()])
    participant_names.short_description = 'Participantes'

    def last_message_preview(self, obj):
        if obj.last_message:
            return obj.last_message.content[:50]
        return '-'
    last_message_preview.short_description = 'Última Mensagem'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'room', 'message_type', 'content_preview', 'is_read', 'created_at')
    list_filter = ('message_type', 'is_read')
    search_fields = ('sender__email', 'content')
    raw_id_fields = ('room', 'sender')

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Conteúdo'
