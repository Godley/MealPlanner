# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from meals.models import Stock, Recipe
from scrapy_djangoitem import DjangoItem


class StockItem(DjangoItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    django_model=Stock

class RecipeItem(DjangoItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    django_model=Recipe
