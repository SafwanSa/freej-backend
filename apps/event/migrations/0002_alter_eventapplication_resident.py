# Generated by Django 4.0.2 on 2022-03-08 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campus', '0002_alter_building_supervisor'),
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventapplication',
            name='resident',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events_applications', to='campus.residentprofile'),
        ),
    ]
