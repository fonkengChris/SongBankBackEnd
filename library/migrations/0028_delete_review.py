# Generated by Django 4.2 on 2023-05-01 01:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0027_song_downloads_song_likes'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Review',
        ),
    ]
