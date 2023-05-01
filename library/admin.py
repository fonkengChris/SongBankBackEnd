from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models
from .models import PreviewImage


class PreviewImageInline(admin.TabularInline):
    model = PreviewImage
    list_display = ['id', 'preview_image']


# class ReviewInline(admin.TabularInline):
#     model = models.Review


class ImagePreviewInline(admin.TabularInline):
    model = models.PreviewImage
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.document.name != '':
            body = f'<iframe src="{instance.document.url}" class="thumbnail"> </iframe>'

            return format_html(body)
        return ''


class DocumentSongInline(admin.TabularInline):
    model = models.DocumentSongFile


class AudioSongInline(admin.TabularInline):
    model = models.AudioSongFile


@admin.register(models.Song)
class SongAdmin(admin.ModelAdmin):
    autocomplete_fields = ['category']
    prepopulated_fields = {
        'slug': ['title']
    }
    inlines = [DocumentSongInline, AudioSongInline]
    list_display = ['title', 'category_title']
    list_filter = ['category', 'last_update']
    list_per_page = 20
    list_select_related = ['category']
    search_fields = ['title']

    def category_title(self, song):
        return song.category.title

    class Media:
        css = {
            'all': ['style.css']
        }


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 20
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']


@admin.register(models.Notation)
class NotationAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    prepopulated_fields = {
        'slug': ['title']
    }
