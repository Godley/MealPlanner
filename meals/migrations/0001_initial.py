# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.FloatField(blank=True)),
                ('instruction', models.CharField(max_length=40, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=20)),
                ('instructions', models.TextField()),
                ('portions', models.IntegerField(default=2)),
                ('marinade_time', models.DurationField(default=datetime.timedelta(0))),
                ('prep_time', models.DurationField(default=datetime.timedelta(0))),
                ('cook_time', models.DurationField(default=datetime.timedelta(0))),
                ('category', models.ForeignKey(default=None, to='meals.Category', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.FloatField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='StockItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('link', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('nickname', models.CharField(max_length=10, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Utensil',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.AddField(
            model_name='stock',
            name='item',
            field=models.ForeignKey(to='meals.StockItem'),
        ),
        migrations.AddField(
            model_name='stock',
            name='units',
            field=models.ForeignKey(blank=True, to='meals.Unit', null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='utensils',
            field=models.ManyToManyField(to='meals.Utensil', blank=True),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='item',
            field=models.ForeignKey(to='meals.StockItem'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='recipe',
            field=models.ForeignKey(to='meals.Recipe'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='units',
            field=models.ForeignKey(blank=True, to='meals.Unit', null=True),
        ),
    ]
