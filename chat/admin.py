from django.contrib import admin
from chat.models import Notification,ChatMessage,ChatThread

# Register your models here.
admin.site.register(Notification)
admin.site.register(ChatMessage)
admin.site.register(ChatThread)