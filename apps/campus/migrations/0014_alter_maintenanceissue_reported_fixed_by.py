# Generated by Django 4.0.2 on 2022-04-27 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campus', '0013_alter_campus_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintenanceissue',
            name='reported_fixed_by',
            field=models.ManyToManyField(blank=True, related_name='reported_fixed_issues', to='campus.ResidentProfile'),
        ),
    ]