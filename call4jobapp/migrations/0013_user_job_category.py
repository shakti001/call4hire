# Generated by Django 4.1.6 on 2023-02-21 07:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('call4jobapp', '0012_jobcategory_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='job_category',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='jobcat', to='call4jobapp.jobcategory'),
            preserve_default=False,
        ),
    ]
