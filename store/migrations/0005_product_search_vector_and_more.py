# Generated by Django 5.1.1 on 2025-01-03 02:05

import django.contrib.postgres.search
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0004_wishlist"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="search_vector",
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(
                fields=["search_vector"], name="store_produ_search__ad07e0_idx"
            ),
        ),
    ]
