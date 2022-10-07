from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import json
from chat.models import Chat, Contact


def get_last_10_messages(chatid):
    chat = get_object_or_404(Chat, id=chatid)
    return chat.messages.order_by("-created_at").all()


# def get_last_10_messages(chatId):
#     chat = get_object_or_404(Chat, id=chatId)
#     return chat.messages.order_by("-timestamp").all()[:10]


def get_user_contact(username):
    user = get_object_or_404(User, username=username)
    return get_object_or_404(Contact, user=user)


# def get_current_chat(chatId):
#     return get_object_or_404(Chat, id=chatId)


def index(request):
    chat = Chat.objects.filter(
        messages__isnull=False,
        participants__in=[request.user],
    ).distinct()

    contacts = Contact.objects.filter(
        user=request.user,
    )
    context = {
        "chats": chat,
        "contacts": contacts,
    }
    return render(request, "chat/index.html", context)


# Chats Above will not be displayed if they dont have message

# create a new chat
def new_chat(request, username):
    user_contact = get_user_contact(username)
    chat = Chat.objects.filter(
        participants__in=[request.user, user_contact.user],
    )
    if chat.exists():
        print(user_contact)
        print("Chat", chat)
    else:
        chat = Chat.objects.create()
        chat.participants.add(user_contact.user)
        chat.participants.add(request.user)
    # redirect to the room
    # return redirect("chat:room", chat.id)
    return redirect("chat:room", chat[0].id)


@login_required
def room(request, room_name):
    get_last_10_messages(room_name)
    context = {
        "room_name": room_name,
        "username": request.user.username,
    }
    return render(request, "chat/room.html", context)
