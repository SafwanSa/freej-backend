# Generated by Django 4.0.2 on 2022-04-02 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventapplication',
            old_name='resident',
            new_name='resident_profile',
        ),
    ]
