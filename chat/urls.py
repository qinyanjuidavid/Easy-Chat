from django.urls import path
from chat import views
from chat.views import new_chat

app_name = "chat"


urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
    path("new_chat/<str:username>/", new_chat, name="new_chat"),
]
