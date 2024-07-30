# Generated by Django 5.0.3 on 2024-05-14 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='status',
            field=models.CharField(choices=[('AV', 'Available'), ('SO', 'Sold')], default='AV', max_length=2),
        ),
    ]