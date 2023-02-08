from .models import Post, Category
from django.contrib.auth.models import User
import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_email_news_celery(idx):
    p = Post.objects.filter(pk=idx).values('isCategory', 'main_text')
    for category in p:
        if category['isCategory']:
            subscribers = Category.objects.filter(id=category['isCategory']).values('subscribers')
            email_list = []
            print('subs', subscribers)
            for name in subscribers:
                if name['subscribers']:
                    user_email = User.objects.get(pk=name['subscribers']).email
                    email_list.append(user_email)
            print(email_list)
            email_uniq = list(set(email_list))
            print(email_uniq)

            subject = 'Новая публикация на нашем сайте!'

            html_content = render_to_string(
                'mail/simple_mail.html',
                {
                    'msg': {
                        'message': category['main_text'],
                        'post_id': idx,
                    },
                }
            )

            msg_prop = EmailMultiAlternatives(
                subject=subject,
                body='Новость в категории!',
                from_email='help@psymphony.ru',
                to=email_uniq,
            )
            msg_prop.attach_alternative(html_content, "text/html")

            msg_prop.send()


# def send_email_news(instance):
#     p = Post.objects.filter(pk=instance.pk).values('isCategory')
#     for category in p:
#         if category['isCategory']:
#             subscribers = Category.objects.filter(id=category['isCategory']).values('subscribers')
#             email_list = []
#             print('subs', subscribers)
#             for name in subscribers:
#                 if name['subscribers']:
#                     user_email = User.objects.get(pk=name['subscribers']).email
#                     email_list.append(user_email)
#             print(email_list)
#             email_uniq = list(set(email_list))
#             print(email_uniq)
#
#             subject = 'Новая публикация на нашем сайте!'
#
#             html_content = render_to_string(
#                 'mail/simple_mail.html',
#                 {
#                     'msg': {
#                         'message': instance.main_text,
#                         'post_id': instance.pk,
#                     },
#                 }
#             )
#
#             msg_prop = EmailMultiAlternatives(
#                 subject=subject,
#                 body='Новость в категории!',
#                 from_email='help@psymphony.ru',
#                 to=email_uniq,
#             )
#             msg_prop.attach_alternative(html_content, "text/html")
#
#             #msg_prop.send()


def send_email_7days():
    now = datetime.datetime.now() - datetime.timedelta(days=7)
    now_format = now.strftime("%Y-%m-%d %H:%M:%S")

    post_detail = {}
    posts = Post.objects.filter(kind='NEWS', date__gt=now_format).order_by('-date').values('title', 'date', 'pk', 'isCategory')
    for post in posts:
        subscriber = Category.objects.filter(id=post['isCategory']).values('subscribers', 'name')
        if subscriber:
            for sub in subscriber:
                if sub['subscribers']:
                    email = User.objects.get(pk=sub['subscribers']).email
                    post_info = {
                        'tittle': post['title'],
                        'link': post['pk'],
                        'category': sub['name'],
                        'date': post['date'].strftime('%Y-%m-%d %H:%M'),
                    }
                    if email not in post_detail:
                        post_detail[email] = []
                    post_detail[email].append(post_info)

    send_to_list = post_detail.keys()
    subject = 'Новости за прошедшую неделю'
    for user_id, user in enumerate(list(send_to_list)):
        post_list_to_html = []
        for idx, post in enumerate(post_detail[user]):  # get unique post (delete post categories)
            if post['tittle'] != post_detail[user][idx-1]['tittle']:
                post_list_to_html.append(post)

        user_email = [list(send_to_list)[user_id]]

        html_content = render_to_string(
            'mail/news_list.html',
            {
                'msg': post_list_to_html,
            }
        )

        msg_prop = EmailMultiAlternatives(
            subject=subject,
            body='Список новостей',
            from_email='help@psymphony.ru',
            to=user_email,
        )
        msg_prop.attach_alternative(html_content, "text/html")

        print(f'email sended to {user_email}')
        msg_prop.send()
