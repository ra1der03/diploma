from typing import Type

import json
from app.tasks import password_reset_task, new_user_task, new_order_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import Signal, receiver
from django_rest_passwordreset.signals import reset_password_token_created

from app.models import User, ConfirmEmailToken

new_user_registered = Signal()
new_order = Signal()


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
    email_ = reset_password_token.user.email
    token_ = reset_password_token.key
    set_ = settings.EMAIL_HOST_USER
    password_reset_task.delay(email_, token_, set_)


@receiver(post_save, sender=User)
def new_user_registered_signal(sender: Type[User], instance: User, created: bool, **kwargs):
    if created and not instance.is_active:
        token, _ = ConfirmEmailToken.objects.get_or_create(user_id=instance.pk)
        email_ = instance.email
        token_ = token.key
        set_ = settings.EMAIL_HOST_USER
        new_user_task.delay(email_, token_, set_)


@receiver(new_order)
def new_order(user_id, **kwargs):
    user = User.objects.get(id=user_id)
    email_ = user.email
    set_ = settings.EMAIL_HOST_USER
    new_order_task.delay(email_, set_)

