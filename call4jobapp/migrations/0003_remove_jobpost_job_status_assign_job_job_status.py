# Generated by Django 4.1.6 on 2023-02-14 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('call4jobapp', '0002_assign_job'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobpost',
            name='job_status',
        ),
        migrations.AddField(
            model_name='assign_job',
            name='job_status',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
