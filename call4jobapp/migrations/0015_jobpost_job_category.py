# Generated by Django 4.1.6 on 2023-02-21 09:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('call4jobapp', '0014_alter_user_job_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpost',
            name='job_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jobcategory', to='call4jobapp.jobcategory'),
        ),
    ]
