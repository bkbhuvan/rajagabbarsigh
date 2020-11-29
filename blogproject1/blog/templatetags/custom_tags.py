from django import template
from blog.models import Post,Comment
register=template.Library()
from django.db.models import Count

@register.simple_tag
def total_post():
    return Post.objects.count()

@register.inclusion_tag('blog/latest_post123.html')
def show_latest_posts():
    latest_posts=Post.objects.order_by('-publish')[:4]
    return {'latest_posts':latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]