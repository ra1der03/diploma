# Generated by Django 5.0.6 on 2024-11-22 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_alter_product_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="productinfo",
            old_name="rrc_price",
            new_name="price_rrc",
        ),
    ]
