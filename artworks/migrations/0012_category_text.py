# Generated by Django 4.2.1 on 2023-06-02 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0011_image_public_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='text',
            field=models.TextField(blank=True, default=''),
        ),
    ]
