from django.contrib import admin
from .models import ArticleR

# Register your models here.
@admin.register(ArticleR)
class ArticleAdmin(admin.ModelAdmin):
    list_display = "id", "title", "body", "published_at"