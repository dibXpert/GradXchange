# Generated by Django 5.0.3 on 2024-04-24 14:02

import django.db.models.deletion
import taggit.managers
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0005_alter_service_service_image'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='service_detail',
            field=models.CharField(default=1, max_length=2000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='service',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now=True)),
                ('commented_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_comments', to=settings.AUTH_USER_MODEL)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='service.service')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]