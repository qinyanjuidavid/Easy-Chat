from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class TrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Contact(TrackingModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(
        "self",
        blank=True,
    )

    class Meta:
        verbose_name_plural = "Contacts"

    def __str__(self):
        return self.user.username


class Message(TrackingModel):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    message = models.TextField(_("message"), blank=True, null=True)
    file = models.FileField(_("file"), upload_to="chat_files", blank=True, null=True)
    is_read = models.BooleanField(_("read"), default=False)
    is_delivered = models.BooleanField(_("delivered"), default=False)
    is_seen = models.BooleanField(_("seen"), default=False)

    class Meta:
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"{self.contact.user.email} "


class Chat(TrackingModel):
    messages = models.ManyToManyField(Message, blank=True)
    participants = models.ManyToManyField(User, blank=True)

    class Meta:
        verbose_name_plural = "Chats"

    def __str__(self):
        return str(self.pk)
