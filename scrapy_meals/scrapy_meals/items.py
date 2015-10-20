# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
import sys, os
from meals.models import Stock

class StockItem(DjangoItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    django_model = Stock
