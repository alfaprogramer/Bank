# Generated by Django 4.0.3 on 2024-01-22 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='address',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, upload_to='profile_images/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='mcode',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
