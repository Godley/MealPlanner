# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('quantity', models.IntegerField(default=0)),
                ('weight', models.IntegerField(default=0)),
                ('recipes', models.ManyToManyField(to='meals.Recipe')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='stockitem',
            name='recipes',
        ),
        migrations.DeleteModel(
            name='StockItem',
        ),
    ]
