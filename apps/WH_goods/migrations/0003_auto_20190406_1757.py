# Generated by Django 2.0 on 2019-04-06 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WH_goods', '0002_auto_20190406_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='prices',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='goods',
            name='sales',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
