# Generated by Django 5.0.3 on 2024-03-09 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0006_item_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_image',
            field=models.ImageField(default='https://neurosoft.com/img/notfound.png', max_length=500, upload_to=''),
        ),
    ]