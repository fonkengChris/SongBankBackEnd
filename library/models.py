from django.db import models
from django.contrib import admin
from django.conf import settings
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from library.validators import FileValidator


class Category(models.Model):
    title = models.CharField(max_length=255)
    # featured_song = models.ForeignKey('Song', on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Notation(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Song(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    author_name = models.CharField(max_length=255, default="Unknown")
    description = models.TextField(null=True, blank=True)
    last_update = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='songs')
    notation = models.ForeignKey(
        Notation, on_delete=models.PROTECT, related_name='songs', default=1)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class DocumentSongFile(models.Model):
    validate_file = FileValidator(
        max_size=1024 * 1000, content_types=('application/pdf', 'application/msword'))
    song = models.ForeignKey(
        Song, on_delete=models.CASCADE, related_name='document_files')
    document_file = models.FileField(
        upload_to='library/document_files', null=True, validators=[validate_file])


class AudioSongFile(models.Model):
    validate_file = FileValidator(
        max_size=1024 * 100, content_types=('application/mp3', 'application/wav'))
    song = models.ForeignKey(
        Song, on_delete=models.CASCADE, related_name='audio_files')
    audio_file = models.FileField(
        upload_to='library/audio_files', null=True, validators=[validate_file])


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


class Review(models.Model):
    song = models.ForeignKey(
        Song, on_delete=models.CASCADE, related_name='reviews')
    description = models.TextField()
    date = models.DateField(auto_now_add=True)


class PreviewImage(models.Model):
    # your fields here
    preview_image = models.ImageField(upload_to='image_previews/', blank=True)
    document_file = models.ForeignKey(
        Song, on_delete=models.CASCADE, related_name='preview_image')

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     if self.document_model.document_file and not self.preview_image:
    #         self.preview_image.save(
    #             f"{self.document_model.document_file.name.split('/')[-1]}.jpg", generate_pdf_preview(self.document_model.document_file), save=False)
    #         self.save(update_fields=['preview_image'])
