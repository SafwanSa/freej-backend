# Generated by Django 4.0.2 on 2022-04-27 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_eventimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventimage',
            old_name='post',
            new_name='event',
        ),
    ]