# Generated by Django 4.1.6 on 2023-04-27 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('call4jobapp', '0031_rename_fcm_token_user_device_token_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'permissions': (('sidebar_blog', 'Can sidebar blog'),)},
        ),
        migrations.AlterModelOptions(
            name='cms_pages',
            options={'permissions': (('sidebar_cms_pages', 'Can sidebar cms_pages'),)},
        ),
    ]
