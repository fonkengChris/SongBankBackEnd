from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from library.admin import AudioSongInline, DocumentSongInline, ImagePreviewInline, ReviewInline, SongAdmin
from library.models import Song
from .models import User
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["email"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", "password", "is_active", "is_staff"]


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email"]
    list_filter = ["email"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        # ("Permissions", {"fields": ["is_admin"]}),
    ]

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("password1", "password2", "email", "first_name", "last_name"),
            },
        ),
    )

    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


# class TagInLine(GenericTabularInline):
#     autocomplete_fields = ['tag']
#     model = TaggedItem
#     extra = 0


class CustomSongAdmin(SongAdmin):
    inlines = [DocumentSongInline, AudioSongInline,
               ReviewInline, ImagePreviewInline]


admin.site.unregister(Song)
admin.site.register(Song, CustomSongAdmin)
