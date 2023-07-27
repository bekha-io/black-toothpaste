from django.contrib import admin

from .models import Post, Tag, Image

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "article_title", "created_by", "created_at", "tags"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass