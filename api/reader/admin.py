from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Article,Media

# Register your models here.
# Register your models here.
class MediaAdmin(admin.ModelAdmin):
    list_display = ('name', 'homepage') # list


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date') # list


admin.site.register(Media,MediaAdmin)
admin.site.register(Article,ArticleAdmin)