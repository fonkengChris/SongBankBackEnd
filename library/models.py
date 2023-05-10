from django.db import models
from django.contrib import admin
from django.conf import settings
from django_countries.fields import CountryField
from django_fulltext_search import SearchManager
from django.core.validators import FileExtensionValidator
from phonenumber_field.modelfields import PhoneNumberField
from library.validators import FileValidator


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Notation(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Language(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']


class Song(models.Model):
    ''' Song model. '''

    # Enable full-text search support for first_name and last_name fields.
    objects = SearchManager(['title', 'author_name', 'lyrics'])

    title = models.CharField(max_length=255)
    slug = models.SlugField()
    author_name = models.CharField(max_length=255, default="Unknown")
    description = models.TextField(null=True, blank=True)
    last_update = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name='likes')
    lyrics = models.TextField()
    language = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name='songs')
    views = models.IntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='songs')
    notation = models.ForeignKey(
        Notation, on_delete=models.CASCADE, related_name='songs', default=1)
    metacritic = models.IntegerField(blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title', 'last_update', 'metacritic']


class DocumentSongFile(models.Model):
    validate_file = FileValidator(
        max_size=1024 * 10000, content_types=('application/pdf'))
    song = models.ForeignKey(
        Song, on_delete=models.CASCADE, related_name='document_files')
    document_file = models.FileField(
        upload_to='library/document_files', null=True, validators=[validate_file, FileExtensionValidator(allowed_extensions=['pdf'])])


class AudioSongFile(models.Model):
    validate_file = FileValidator(
        max_size=1024 * 20000, content_types=('audio/mp3', 'audio/mpeg', 'audio/ogg'))
    song = models.ForeignKey(
        Song, on_delete=models.CASCADE, related_name='audio_files')
    audio_file = models.FileField(
        upload_to='library/audio_files', null=True, validators=[validate_file])


class PreviewImage(models.Model):
    # your fields here
    preview_image = models.ImageField(
        upload_to='library/preview_images/', blank=True)
    song = models.ForeignKey(
        Song, on_delete=models.CASCADE, related_name='preview_image')


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold')
    ]

    phone = PhoneNumberField(blank=True)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    country = CountryField(default="EN")
    favourite_list = models.ManyToManyField(
        Song, blank=True, related_name='my_list')
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        permissions = [
            ('view_history', 'Can view history')
        ]
