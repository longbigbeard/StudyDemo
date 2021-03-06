# Generated by Django 2.0 on 2019-04-11 16:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuidfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('WH_goods', '0003_auto_20190406_1757'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsOrder',
            fields=[
                ('uid', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('amount', models.FloatField(default=0)),
                ('pub_time', models.DateTimeField(auto_now_add=True)),
                ('istype', models.SmallIntegerField(default=0)),
                ('status', models.SmallIntegerField(default=1)),
                ('order_info', models.TextField(null=True)),
                ('order_tel', models.CharField(max_length=11, null=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='WH_goods.Goods')),
            ],
        ),
    ]
