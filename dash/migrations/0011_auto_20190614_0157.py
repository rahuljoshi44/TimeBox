# Generated by Django 2.2.1 on 2019-06-14 01:57

import dash.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0010_auto_20190614_0141'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='active_expiry',
            field=models.DateField(default=dash.models.set_active_expiry),
        ),
        migrations.AddField(
            model_name='task',
            name='final_expiry',
            field=models.DateField(default=dash.models.set_final_expiry),
        ),
    ]
