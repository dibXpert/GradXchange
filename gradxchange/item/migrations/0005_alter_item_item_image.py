# Generated by Django 5.0.2 on 2024-03-01 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0004_alter_item_item_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_image',
            field=models.CharField(default='https://neurosoft.com/img/notfound.png', max_length=500),
        ),
    ]