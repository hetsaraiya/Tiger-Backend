# Generated by Django 5.0.3 on 2024-03-13 03:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0005_remove_store_image_urls"),
    ]

    operations = [
        migrations.AlterField(
            model_name="store",
            name="link",
            field=models.CharField(max_length=500, unique=True),
        ),
    ]
