# Generated by Django 5.0.3 on 2024-03-12 13:44

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_product_category_product_subcategory"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="card_type",
        ),
    ]
