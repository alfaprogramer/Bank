# Generated by Django 4.0.3 on 2024-01-29 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0004_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]