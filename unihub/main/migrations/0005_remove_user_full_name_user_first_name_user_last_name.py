# Generated by Django 5.2 on 2025-05-07 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='full_name',
        ),
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(default='Text', max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(default='Text', max_length=255),
        ),
    ]
