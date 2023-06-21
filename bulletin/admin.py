from django.contrib import admin
from .models import Bulletin, Comment

# Register your models here.

class BulletinAdmin(admin.ModelAdmin):
    list_display = ("title", "poster", "content", "post_Date", "update_Date")

admin.site.register(Bulletin, BulletinAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "content", "post_Date")

admin.site.register(Comment, CommentAdmin)
