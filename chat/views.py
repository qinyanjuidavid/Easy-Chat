from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import json
from chat.models import Chat


def get_last_10_messages(chatid):
    chat = get_object_or_404(Chat, id=chatid)
    return chat.messages.order_by("-timestamp").all()[:10]


def index(request):
    usersObj = User.objects.all()
    context = {"users": usersObj}
    return render(request, "chat/index.html", context)


@login_required
def room(request, room_name):
    context = {"room_name": room_name, "username": request.user.username}
    return render(request, "chat/room.html", context)


# def indexJson(request):
#     usersObj = User.objects.all()
#     userList = []
#     for user in usersObj:
#         item = {
#             "username": user.username,
#             "id": user.id

#         }
#         userList.append(item)
#     context = {
#         "users": userList
#     }
#     return JsonResponse(context)


# def userGetJson(request):
#     if request.is_ajax():
#         pk = request.POST.get("pk")
#         userQs = User.objects.get(id=int(pk))
#         userObj = {
#             "username": userQs.username,
#             "id": userQs.id
#         }
#         context = {
#             "user": userObj
#         }
#         return JsonResponse(context)
#     return JsonResponse({"success": "false"})
