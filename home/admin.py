from django.contrib import admin
from django.utils.html import format_html
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'short_message', 'status', 'colored_status', 'created_at')
    list_editable = ('status',)
    search_fields = ('name', 'email', 'message')
    list_filter = ('status', 'created_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    @admin.display(description='Message')
    def short_message(self, obj):
        if len(obj.message) > 50:
            return obj.message[:50] + '...'
        return obj.message
 
    @admin.display(description='Status Color')
    def colored_status(self, obj):
        if obj.status == 'new':
            return format_html(
                '<span style="color: red; font-weight: bold;">● {}</span>',
                'New'
            )
        elif obj.status == 'read':
            return format_html(
                '<span style="color: blue; font-weight: bold;">● {}</span>',
                'Read'
            )
        elif obj.status == 'replied':
            return format_html(
                '<span style="color: purple; font-weight: bold;">● {}</span>',
                'Replied'
            )
        return obj.status
    