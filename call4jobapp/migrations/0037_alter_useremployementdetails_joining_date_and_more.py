# Generated by Django 4.2 on 2023-06-06 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('call4jobapp', '0036_alter_useremployementdetails_joining_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useremployementdetails',
            name='joining_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='useremployementdetails',
            name='leaving_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]