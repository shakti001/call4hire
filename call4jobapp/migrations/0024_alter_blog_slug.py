# Generated by Django 4.1.6 on 2023-03-02 11:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('call4jobapp', '0023_blog_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='slug',
            field=models.CharField(blank=True, default=uuid.uuid4, max_length=50, null=True, unique=True),
        ),
    ]
