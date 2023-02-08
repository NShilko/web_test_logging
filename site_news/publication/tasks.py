from celery import shared_task
from .send_email import send_email_7days, send_email_news_celery


@shared_task
def send_week_news():
    send_email_7days()


@shared_task
def send_new_news(idx):
    send_email_news_celery(idx)
