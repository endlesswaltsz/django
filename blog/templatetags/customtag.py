from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.template import Library

from blog import models

register = Library()


@register.inclusion_tag('inclusion_tag.html')
def category_and_tag(user):
    blog = models.Blog.objects.filter(userinfo=user)
    category = models.Category.objects.filter(blog=blog).annotate(c=Count('article')).values_list('name', 'c', 'pk')
    tag = models.Tag.objects.filter(blog=blog).annotate(c=Count('article')).values_list('name', 'c', 'pk')
    time_article = models.Article.objects.filter(blog=blog).annotate(time=TruncMonth('upload_time')).values(
        'time').annotate(
        c=Count('time')).values_list('time', 'c', 'time')
    return {'category': category, 'tag': tag, 'time_article': time_article, 'user': user}


@register.filter()
def length(lis):
    return len(lis)
