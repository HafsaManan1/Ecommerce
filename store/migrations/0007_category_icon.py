# Generated by Django 5.1.1 on 2025-01-03 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0006_remove_product_store_produ_search__ad07e0_idx_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="icon",
            field=models.ImageField(null=True, upload_to="images/"),
        ),
    ]
