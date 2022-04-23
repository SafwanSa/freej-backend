# Generated by Django 4.0.2 on 2022-04-23 18:21

import core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commercialannouncement',
            name='image',
            field=models.FileField(blank=True, max_length=2048, null=True, upload_to=core.utils.PathAndRename('uploads/commercials/images/2022/04/23')),
        ),
    ]