# Generated by Django 4.2 on 2023-04-14 22:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0014_remove_review_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreviewImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preview_image', models.ImageField(blank=True, upload_to='pdf_previews/')),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preview_images', to='library.song')),
            ],
        ),
    ]