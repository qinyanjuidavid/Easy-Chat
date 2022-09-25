from django.urls import path
from chat import views

app_name = "chat"


urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
    # path("index/json/", views.indexJson, name="indexJson"),
    # path("user/json/", views.userGetJson, name="userJson"),
]
