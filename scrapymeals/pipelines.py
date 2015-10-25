# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# -*- coding: utf-8 -*-
import re
from meals.models import Stock, Recipe
import re
from bs4 import BeautifulSoup
from django.db.models import Q



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
                name_list = name.split(" ")
                try:
                    model = Stock.objects.get(title=name)

                except:
                    try:
                        model = Stock.objects.filter(reduce(lambda x, y: x | y, [Q(name__contains=word) for word in name_list]))[0:1]
                    except:
                        model = Stock.objects.create(title=name)
                model.recipes.add(recipe)
                model.save()
        return ritem

    def parse_stock_name(self, stockname):
        souped = BeautifulSoup(stockname)
        stock_text = souped.get_text()
        words = stock_text.split(" ")
        indicator = 0
        quantity = words[indicator]
        pattern = re.compile('[0-9]+[a-z]*[A-Z]*')
        if pattern.findall(quantity):
            indicator = 1
        unit = ""
        units = ['g', 'ml', 'kg', 'cups', 'cup', 'grams', 'can', 'tbsp', 'tsp', 'tbsps', 'tsps',
                 'small', 'bunch', 'piece', 'handful', 'pack', 'chopped', 'large', 'a', 'pinch',
                 'fresh', 'dried', 'heaped', 'thick', 'slices', 'slice']
        while words[indicator] in units:
            unit += " "+words[indicator]
            indicator += 1
        remainder = " ".join(words[indicator:])
        instructions = remainder.split(",")
        item = instructions[0]
        if item.endswith("s"):
            item = item[:len(item)-1]
        direction = ",".join(instructions[1:])

        return quantity, item, direction

