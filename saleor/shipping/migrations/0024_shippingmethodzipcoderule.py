# Generated by Django 3.1.3 on 2020-11-30 13:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shipping", "0023_shippingmethod_excluded_products"),
    ]

    operations = [
        migrations.CreateModel(
            name="ShippingMethodZipCodeRule",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start", models.CharField(max_length=32)),
                ("end", models.CharField(blank=True, max_length=32, null=True)),
                (
                    "shipping_method",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="zip_code_rules",
                        to="shipping.shippingmethod",
                    ),
                ),
            ],
            options={
                "unique_together": {("shipping_method", "start", "end")},
            },  # noqa
        ),
    ]
