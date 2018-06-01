from django.contrib import admin

# Register your models here.

from core.models import  Word,UserProfile

# class UserAdmin(admin.ModelAdmin):
#     list_display = ('name', 'homepage') # list
#
#
# class WordAdmin(admin.ModelAdmin):
#     list_display = ('title', 'pub_date') # list
#
#
# admin.site.register(Media,MediaAdmin)
# admin.site.register(Article,ArticleAdmin)

admin.site.register(Word)
admin.site.register(UserProfile)