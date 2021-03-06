# Generated by Django 2.0 on 2019-04-06 07:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, null=True)),
                ('seals', models.CharField(max_length=100, null=True)),
                ('prices', models.CharField(max_length=100, null=True)),
                ('goods_info', models.TextField(null=True)),
                ('feature_info', models.TextField(null=True)),
                ('schedule_goods', models.TextField(null=True)),
                ('attention_goods', models.TextField(null=True)),
                ('thumbnail', models.URLField(null=True)),
                ('goods_video', models.URLField(null=True)),
                ('pub_time', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['seals'],
            },
        ),
    ]
