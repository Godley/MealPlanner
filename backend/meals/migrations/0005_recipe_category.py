# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-19 15:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0004_recipe_sides'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='category',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
