# Generated by Django 4.2 on 2023-04-19 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0024_song_metacritic'),
    ]

    operations = [
        migrations.AddField(
            model_name='notation',
            name='slug',
            field=models.SlugField(default='-'),
            preserve_default=False,
        ),
    ]