# Generated by Django 5.1.5 on 2025-02-03 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_newspaperissue_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='newspaperissue',
            name='featured',
            field=models.BooleanField(default=False, verbose_name='Featured'),
        ),
    ]
