# Generated by Django 4.1.6 on 2023-03-02 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('call4jobapp', '0021_blog'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=300, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
