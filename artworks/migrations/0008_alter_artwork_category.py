# Generated by Django 4.2.1 on 2023-05-29 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0007_alter_artwork_image_alter_page_banner_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artwork',
            name='category',
            field=models.ManyToManyField(blank=True, to='artworks.category'),
        ),
    ]