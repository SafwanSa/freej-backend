# Generated by Django 4.0.2 on 2022-04-26 02:11

import core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campus', '0010_alter_residentprofile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campus',
            name='image',
            field=models.FileField(blank=True, max_length=2048, null=True, upload_to=core.utils.PathAndRename('uploads/campuses/images/2022/04/26')),
        ),
    ]
