# Generated by Django 4.2.4 on 2023-10-20 23:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_product_is_description_html"),
    ]

    operations = [
        migrations.AddField(
            model_name="productcategory",
            name="is_description_html",
            field=models.BooleanField(default=False),
        ),
    ]