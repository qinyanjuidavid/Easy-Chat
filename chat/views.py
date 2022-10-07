from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import json
from chat.models import Chat, Contact
from django.db.models import Q


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


@login_required
def index(request):
    chat = Chat.objects.filter(
        # messages__isnull=False,
        participants__in=[request.user],
    ).distinct()

    contacts = Contact.objects.filter(
        user=request.user,
    )

    users = User.objects.exclude(id=request.user.id)
    context = {
        "users": users,
        "chats": chat,
        "contacts": contacts,
    }
    return render(request, "chat/index.html", context)


# Create Contact
# def new_contact(request, username):
#     contact_query, _ = Contact.objects.get_or_create(
#         user=request.user,
#     )


# create a new chat
@login_required
def new_chat(request, username):
    user_contact = get_user_contact(username)
    chats = Chat.objects.filter(
        participants__in=[request.user],
    ).distinct()

    for chat in chats:
        if user_contact.user in chat.participants.all():
            return redirect("chat:room", chat.id)

    chat = Chat.objects.create()
    chat.participants.add(request.user, user_contact.user)
    chat.save()
    return redirect("chat:room", chat.id)


@login_required
def room(request, room_name):
    get_last_10_messages(room_name)
    context = {
        "room_name": room_name,
        "username": request.user.username,
    }
    return render(request, "chat/room.html", context)
