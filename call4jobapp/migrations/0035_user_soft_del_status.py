# Generated by Django 4.1.6 on 2023-05-08 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('call4jobapp', '0034_alter_jobcategory_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='soft_del_status',
            field=models.BooleanField(default=False),
        ),
    ]
