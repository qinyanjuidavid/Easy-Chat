from django.contrib import admin
from chat.models import Message


@admin.register(Message)
class MyAdminMessage(admin.ModelAdmin):
    list_display = ["contact", "timestamp"]
