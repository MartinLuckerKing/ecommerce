# Generated by Django 4.0.4 on 2022-09-26 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_alter_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, upload_to='products/%Y/%m/%d'),
        ),
    ]
