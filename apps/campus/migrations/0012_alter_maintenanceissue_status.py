# Generated by Django 4.0.2 on 2022-04-26 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campus', '0011_alter_campus_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintenanceissue',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('canceled', 'Canceled'), ('fixed', 'Fixed')], max_length=30),
        ),
    ]