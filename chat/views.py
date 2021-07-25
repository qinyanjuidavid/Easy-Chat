from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


def index(request):
    context = {

    }
    return render(request, "chat/index.html", context)


def room(request, room_name):
    context = {
        'room_name': room_name
    }
    return render(request, "chat/room.html", context)
