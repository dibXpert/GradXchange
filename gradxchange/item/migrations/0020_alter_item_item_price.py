# Generated by Django 5.0.3 on 2024-04-07 10:11

import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0019_item_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
    ]