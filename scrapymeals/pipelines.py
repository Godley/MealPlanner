# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# -*- coding: utf-8 -*-
import re
from meals.models import Stock, Recipe

class GoodFoodStockPipeline(object):

    def process_item(self, item, spider):
        if type(item) != dict:
            item.save()
            ritem = item
        else:
            ritem = item["item"]
            stock = item["stock"]
            ritem.save()
            recipe = Recipe.objects.get(title=ritem['title'])
            for value in stock:
                quantity, name, direction = self.parse_stock_name(value['title'])
                try:
                    model = Stock.objects.get(title=name)
                except:
                    model = Stock.objects.create(title=name)
                model.recipes.add(recipe)
                model.save()
        return ritem

    def parse_stock_name(self, stockname):
        words = stockname.split(" ")
        print(words)
        quantity = words[0]
        remainder = " ".join(words[1:])
        instructions = remainder.split(",")
        item = instructions[0]
        direction = ",".join(instructions[1:])
        return quantity, item, direction

