"""
agent/urls.py
"""
from django.urls import path
from . import views

app_name = "agent"

urlpatterns = [
    path("chat/", views.agent_chat, name="chat"),
]
