from django.contrib import admin
from chat.models import Message, Contact, Chat


@admin.register(Message)
class MyAdminMessage(admin.ModelAdmin):
    list_display = ["contact", "timestamp"]


admin.site.register(Contact)
admin.site.register(Chat)
