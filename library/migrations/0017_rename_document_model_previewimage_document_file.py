# Generated by Django 4.2 on 2023-04-15 08:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0016_previewimage_alter_documentsongfile_document_file_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='previewimage',
            old_name='document_model',
            new_name='document_file',
        ),
    ]
