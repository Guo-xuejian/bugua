from django.db.models.functions import TruncMonth
from django.template import library
from django.db.models import Count
from blog import models

register = library.Library()


# 侧边栏inclusion_tag
@register.inclusion_tag('Left.html')
def left(username):
    user = models.UserInfo.objects.filter(username=username).first()
    res_category = models.Category.objects.filter(blog=user.blog).annotate(num=Count('article__id')).values_list(
        'name', 'num', 'id')
    res_tag = models.Tag.objects.filter(blog=user.blog).annotate(num=Count('article__id')).values_list('name',
                                                                                                       'num', 'id')
    res_date = models.Article.objects.filter(blog=user.blog).annotate(month=TruncMonth('create_time')).values(
        'month').annotate(c=Count('id')).order_by('-month').values_list('month', 'c')

    return {'name': username, 'res_category': res_category, 'res_tag': res_tag, 'res_date': res_date}
