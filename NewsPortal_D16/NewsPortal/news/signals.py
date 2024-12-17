from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from .models import *
from .tasks import notify_post_created_task


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель


@receiver(post_save, sender=Post)
def notify_post_created(sender, instance, created, **kwargs):
    if created:
        notify_post_created_task.delay(instance.pk)


