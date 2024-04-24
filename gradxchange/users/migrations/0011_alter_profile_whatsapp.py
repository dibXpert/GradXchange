# Generated by Django 5.0.3 on 2024-04-24 13:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_profile_phone_alter_profile_whatsapp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='whatsapp',
            field=models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Whatsapp number must be entered in the format: '+60123456789'. With country code +60 and up to 10 digits allowed.", regex='^\\+?60?\\d{9,10}$')]),
        ),
    ]
