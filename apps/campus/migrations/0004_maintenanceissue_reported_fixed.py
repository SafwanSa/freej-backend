# Generated by Django 4.0.2 on 2022-04-02 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campus', '0003_maintenanceissue'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenanceissue',
            name='reported_fixed',
            field=models.IntegerField(default=0),
        ),
    ]
