# Generated by Django 4.2 on 2023-04-04 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_remove_customer_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='SongFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='library/files')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='library.song')),
            ],
        ),
    ]