# Generated by Django 4.0.4 on 2022-05-08 10:44

import core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campus', '0002_alter_maintenanceissue_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='location_url',
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='building',
            name='whatsApp_link',
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='campus',
            name='image',
            field=models.FileField(max_length=2048, upload_to=core.utils.PathAndRename('uploads/campuses/images/2022/05/08')),
        ),
        migrations.AlterField(
            model_name='campus',
            name='location_url',
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='residentprofile',
            name='photo',
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
    ]
