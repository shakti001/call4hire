# Generated by Django 4.1.6 on 2023-02-16 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('call4jobapp', '0004_remove_assign_job_job_status_jobpost_job_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='work_status',
            field=models.CharField(default='Fresher', max_length=20),
        ),
    ]
