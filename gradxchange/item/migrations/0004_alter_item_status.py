# Generated by Django 5.0.3 on 2024-05-14 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0003_alter_item_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.CharField(choices=[('AV', 'Available'), ('NA', 'Not Available'), ('SO', 'Sold'), ('BO', 'Booked')], default='AV', max_length=2),
        ),
    ]
