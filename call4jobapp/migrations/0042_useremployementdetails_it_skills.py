# Generated by Django 4.1.6 on 2023-06-15 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('call4jobapp', '0041_useremployementdetails_skills_used'),
    ]

    operations = [
        migrations.AddField(
            model_name='useremployementdetails',
            name='it_skills',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
