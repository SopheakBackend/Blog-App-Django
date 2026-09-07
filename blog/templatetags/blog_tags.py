from django import template
from django.utils.safestring import mark_safe
import markdown

from ..models import Post
from django.db.models import Count

register = template.Library()
@register.simple_tag
def total_post():
    return Post.published.count()
@register.inclusion_tag('blog/post/latest_post.html')
def show_latest_posts():
    latest_post = Post.published.order_by('-publish')[:5]
    return {'latest_post': latest_post}
@register.simple_tag
def most_commented_post():
    return Post.published.annotate(
        total_comment = Count('comments')
    ).order_by('-total_comment')[:5]
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))