# Generated by Django 4.2 on 2023-04-18 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0021_alter_previewimage_document_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='previewimage',
            old_name='document_file',
            new_name='song',
        ),
    ]
