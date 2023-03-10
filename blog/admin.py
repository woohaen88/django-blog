from django.contrib import admin
from .models import Post, Category, Tag, Comment

admin.site.register(Post)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Category 모델의 name 필드에 값이 입력됐을 째 자동으로 slug가 만들어짐
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
