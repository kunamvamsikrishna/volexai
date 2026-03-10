from django.shortcuts import render
from rest_framework import generics
from chat.models import ChatSession, Message, Request
from chat.pagination import ChatMessageCursorPagination
from chat.seralizers import ChatsSerializer, MessageSerializer, RequestSerializer
from rest_framework.permissions import IsAuthenticated


class ChatView(generics.ListAPIView):
    serializer_class = ChatsSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user).select_related('model','model__provider').order_by('-created_at')


class ChatMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ChatMessageCursorPagination
    def get_queryset(self):
        return Message.objects.filter(user=self.request.user, chat_session_id=self.kwargs['chat_session_id']).order_by('-created_at')
    

class RequestsView(generics.ListAPIView):
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Request.objects.filter(user=self.request.user,request_type="apicall").select_related('model','model__provider').order_by('-created_at')
    

class UpdateChatTitleView(generics.UpdateAPIView):
    serializer_class = ChatsSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)
    

class DeleteChatView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)