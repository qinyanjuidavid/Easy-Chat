from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json


def index(request):
    context = {

    }
    return render(request, "chat/index.html", context)


def room(request, room_name):
    context = {
        'room_name': room_name
    }
    return render(request, "chat/room.html", context)
