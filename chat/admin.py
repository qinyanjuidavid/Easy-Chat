from django.contrib import admin
from chat.models import Message, Contact, Chat


@admin.register(Message)
class messageAdmin(admin.ModelAdmin):
    list_display = ["contact", "created_at"]


admin.site.register(Contact)
admin.site.register(Chat)
