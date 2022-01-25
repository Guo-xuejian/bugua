from django.contrib import admin

from blog import models

# 注册app，Django内置admin后台管理可见
admin.site.register(models.Log)
admin.site.register(models.Tag)
admin.site.register(models.Blog)
admin.site.register(models.Swiper)
admin.site.register(models.Article)
admin.site.register(models.Comment)
admin.site.register(models.Category)
admin.site.register(models.UserInfo)
admin.site.register(models.UpAndDown)
admin.site.register(models.Tag2Article)
