# Generated by Django 2.0 on 2019-04-05 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WH_scene', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenes',
            name='grade',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
