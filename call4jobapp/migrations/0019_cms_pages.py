# Generated by Django 4.1.6 on 2023-02-28 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('call4jobapp', '0018_assign_job_assign_job_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cms_pages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading1', models.CharField(max_length=200)),
                ('image1', models.ImageField(upload_to='')),
                ('heading2', models.CharField(max_length=200)),
                ('heading3', models.CharField(max_length=200)),
                ('paragraph1', models.CharField(max_length=200)),
                ('paragraph2', models.CharField(max_length=200)),
                ('image2', models.ImageField(upload_to='')),
            ],
        ),
    ]
