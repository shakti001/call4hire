# Generated by Django 4.1.6 on 2023-04-21 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('call4jobapp', '0025_blogcategory_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='country_code',
            field=models.CharField(default='2021-03-27', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='office_address',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
