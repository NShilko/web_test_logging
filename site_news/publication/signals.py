from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import PostCategory
from .send_email import send_email_news_celery


@receiver(m2m_changed, sender=PostCategory)
def notify_news(sender, instance, **kwargs):
    send_email_news_celery(instance.pk)
    #send_email_news(instance)
