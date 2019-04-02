# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-02-15 20:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='sub_floor',
        ),
        migrations.AddField(
            model_name='article',
            name='root_floor_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comment',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default='2018-1-1 12:00:00'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='parent_floor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Comment'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(max_length=200),
        ),
    ]
