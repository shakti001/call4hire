# Generated by Django 4.1.6 on 2023-02-21 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('call4jobapp', '0016_applyjob'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
