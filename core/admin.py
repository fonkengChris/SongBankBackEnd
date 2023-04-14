from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from library.admin import AudioSongInline, DocumentSongInline, ReviewInline, SongAdmin
from library.models import Song
from .models import User

# from django.contrib.contenttypes.admin import GenericTabularInline
# from library.admin import SongAdmin
# from library.models import Song
# from tags.models import TaggedItem


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "email", "first_name", "last_name"),
            },
        ),
    )


# class TagInLine(GenericTabularInline):
#     autocomplete_fields = ['tag']
#     model = TaggedItem
#     extra = 0


class CustomSongAdmin(SongAdmin):
    inlines = [DocumentSongInline, AudioSongInline, ReviewInline]


admin.site.unregister(Song)
admin.site.register(Song, CustomSongAdmin)