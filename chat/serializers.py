from rest_framework import serializers
from .models import ChatThread, ChatMessage, Notification

class ChatMessageSerializer(serializers.ModelSerializer):
    sender_username =   serializers.CharField(source='sender.username',read_only=True)
    sender_name = serializers.CharField(read_only=True)
    class Meta:
        model = ChatMessage
        fields = ['id','thread','sender','sender_username','sender_name','message','is_read','created_at']
        read_only_fields = ['id','created_at','sender_username','sender_name']

class ChatThreadSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    user1_name = serializers.CharField(source = 'user1.username',read_only = True)
    user2_name = serializers.CharField(source = 'user2.username',read_only = True)
    class Meta:
        model = ChatThread
        fields = [  'id', 'user1', 'user1_name','user2','user2_name', 'name','created_at','last_message']
        read_only_fields = ['id','created_at','last_message']
        def get_last_message(self,obj):
            last = obj.messages.last()
            return ChatMessageSerializer(last).data if last else None
        
class NotificationSerializer(serializers.ModelSerializer):
    model = Notification
    fields = ['id','recipient','sender','sender_username','type','message','link','is_read','created_at']
    read_only_fields = ['id','created_at','sender_username']