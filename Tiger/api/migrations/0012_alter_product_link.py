# Generated by Django 5.0.3 on 2024-03-13 04:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0011_product_link"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="link",
            field=models.CharField(default="", max_length=500, unique=True),
        ),
    ]
