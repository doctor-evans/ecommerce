# Generated by Django 5.1.1 on 2024-09-30 15:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0009_alter_product_description_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productreview",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_review",
                to="core.product",
            ),
        ),
    ]
