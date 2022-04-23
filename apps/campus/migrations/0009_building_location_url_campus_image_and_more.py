# Generated by Django 4.0.2 on 2022-04-23 18:21

import core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campus', '0008_alter_maintenanceissue_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='location_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='campus',
            name='image',
            field=models.FileField(blank=True, max_length=2048, null=True, upload_to=core.utils.PathAndRename('uploads/campuses/images/2022/04/23')),
        ),
        migrations.AddField(
            model_name='campus',
            name='location_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='residentprofile',
            name='photo',
            field=models.FileField(blank=True, max_length=2048, null=True, upload_to=core.utils.PathAndRename('uploads/residents/photos/2022/04/23')),
        ),
    ]
