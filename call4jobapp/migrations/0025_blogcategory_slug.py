# Generated by Django 4.1.6 on 2023-03-03 06:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('call4jobapp', '0024_alter_blog_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogcategory',
            name='slug',
            field=models.CharField(blank=True, default=uuid.uuid4, max_length=50, null=True, unique=True),
        ),
    ]
