# Generated by Django 5.1.6 on 2025-02-18 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shorturl',
            name='click_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
