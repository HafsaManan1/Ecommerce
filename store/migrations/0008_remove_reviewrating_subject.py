# Generated by Django 5.1.1 on 2025-01-05 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0007_category_icon"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="reviewrating",
            name="subject",
        ),
    ]
