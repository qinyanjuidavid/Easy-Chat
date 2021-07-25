from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import json

def index(request):
    context = {

    }
    return render(request, "chat/index.html", context)

@login_required
def room(request, room_name):
    context = {
        'room_name': room_name,
        'username':mark_safe(json.dumps(request.user.username))

    }
    return render(request, "chat/room.html", context)
