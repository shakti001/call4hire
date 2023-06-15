# Generated by Django 4.1.6 on 2023-02-21 06:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('call4jobapp', '0011_rename_job_jobcategory_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobcategory',
            name='slug',
            field=models.CharField(default=uuid.uuid4, max_length=50, unique=True),
        ),
    ]