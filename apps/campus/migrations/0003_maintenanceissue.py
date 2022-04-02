# Generated by Django 4.0.2 on 2022-04-02 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campus', '0002_alter_residentprofile_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaintenanceIssue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('type', models.CharField(choices=[('halls', 'Halls'), ('Rooms', 'Rooms'), ('bathroom', 'Bathrooms'), ('other', 'Other')], max_length=30)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('canceled', 'Canceled'), ('fixed', 'Fixed')], max_length=30)),
                ('description', models.TextField()),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='campus.building')),
                ('reported_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported_issues', to='campus.residentprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
