# Generated by Django 4.0.1 on 2022-03-08 18:15

import discuss_api.apps.agenda.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0007_comment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.CharField(choices=[('ACTIVE', '0'), ('DELETED_BY_USER', '1'), ('DELETED_BY_ADMIN', '2'), ('DELETED_BY_WITHDRAWAL', '3')], default=discuss_api.apps.agenda.models.CommentStatus['ACTIVE'], max_length=25),
        ),
    ]