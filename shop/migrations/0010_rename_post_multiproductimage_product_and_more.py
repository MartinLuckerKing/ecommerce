# Generated by Django 4.0.4 on 2022-09-30 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_remove_product_image2_remove_product_image3_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='multiproductimage',
            old_name='post',
            new_name='product',
        ),
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
    ]
