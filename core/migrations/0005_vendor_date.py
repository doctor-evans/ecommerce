# Generated by Django 5.1.1 on 2024-09-27 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_vendor_cover_image_alter_product_vendor"),
    ]

    operations = [
        migrations.AddField(
            model_name="vendor",
            name="date",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]