# Generated by Django 4.2 on 2023-04-18 00:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0020_alter_previewimage_preview_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='previewimage',
            name='document_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preview_image', to='library.song'),
        ),
    ]
