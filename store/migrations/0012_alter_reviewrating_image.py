# Generated by Django 5.1.1 on 2025-01-18 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0011_reviewrating_subject"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reviewrating",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="reviews/"),
        ),
    ]
