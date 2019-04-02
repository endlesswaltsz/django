from django.contrib import admin
from blog import models
# Register your models here.

class Abc(admin.ModelAdmin):
    list_select_related = ['content,title']
admin.site.register(models.Article,Abc)
admin.site.register(models.Blog)
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.UserInfo)
admin.site.register(models.LikeAndAgainst)
admin.site.register(models.Article2Tag)
admin.site.register(models.Comment)