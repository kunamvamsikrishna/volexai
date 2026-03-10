
from django.urls import path
from .views import *

urlpatterns = [
    path('chats/', ChatView.as_view(), name='chat'),
    path('chats/<int:chat_session_id>/messages/', ChatMessagesView.as_view(), name='chat-messages'),
    path("requests/", RequestsView.as_view()),
    path("chats/<int:pk>/   /", UpdateChatTitleView.as_view(), name="update-chat-title"),
    path("chats/<int:pk>/delete/", DeleteChatView.as_view(), name="delete-chat"),
]