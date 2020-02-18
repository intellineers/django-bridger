from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils import timezone
from django.utils.html import strip_tags


# @shared_task
def send_system(notification):
    channel_layer_name = f"notification-{notification.recipient.id}"
    async_to_sync(get_channel_layer().group_send)(
        channel_layer_name,
        {"content": notification.to_payload(), "type": "notification.notify"},
    )


# @shared_task
def send_mail(notification):
    context = {"notification": notification}
    template = getattr(
        settings,
        "BRIDGER_NOTIFICATION_TEMPLATE",
        "bridger/email_notification_template.html",
    )
    email_to = notification.recipient.email
    email_from = getattr(
        settings, "BRIDGER_NOTIFICATION_EMAIL_FROM", "system@bridger.com",
    )
    rendered_template = get_template(template).render(context)

    msg = EmailMultiAlternatives(
        subject=f"Notification {notification.title}",
        body=strip_tags(rendered_template),
        from_email=email_from,
        to=[email_to],
    )
    msg.attach_alternative(rendered_template, "text/html")
    msg.send()

    notification.__class__.objects.filter(id=notification.id).update(
        timestamp_mailed=timezone.now()
    )
