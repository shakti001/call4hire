# Generated by Django 4.1.6 on 2023-04-27 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('call4jobapp', '0033_alter_jobcategory_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jobcategory',
            options={'permissions': (('sidebar_jobcategory', 'Can sidebar jobcategory'),)},
        ),
    ]
