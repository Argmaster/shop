# Generated by Django 4.2.4 on 2023-10-20 23:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="is_description_html",
            field=models.BooleanField(default=False),
        ),
    ]
