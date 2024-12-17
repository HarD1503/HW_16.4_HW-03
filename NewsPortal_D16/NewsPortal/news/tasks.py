from celery import shared_task
from .models import *
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from datetime import timedelta
from django.utils import timezone


@shared_task
def notify_post_created_task(pk):

    post = Post.objects.get(pk=pk)
    categories = post.post_category.all()
    title = post.post_title
    subscribers_emails = []

    for cat in categories:
        subscribers_users = cat.subscribers.all()
        for sub_users in subscribers_users:
            subscribers_emails.append(sub_users.email)

    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': post.preview,
            'link': f'{settings.SITE_URL}/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@shared_task
def notify_weekly_posts_task():
    today = timezone.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(post_time__gte=last_week)
    categories = set(posts.values_list('post_category__category_name', flat=True))
    subscribers = set(Category.objects.filter(category_name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'weekly_posts.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()