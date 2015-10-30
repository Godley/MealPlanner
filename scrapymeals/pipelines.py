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
from inflect import engine
from nltk import word_tokenize, pos_tag




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
                souped = BeautifulSoup(value['title'], "lxml")
                stock_text = souped.get_text()
                value = self.parse_stock_name(stock_text)
                if value is not None:
                    quantity, name, direction = value
                else:
                    return ritem
                name_list = name.split(" ")
                try:
                    model = Stock.objects.get(title=name)

                except:
                    try:
                        model = Stock.objects.filter(reduce(lambda x, y: x | y, [Q(name__contains=word) for word in name_list]))[0:1]
                    except:
                        model = Stock.objects.create(title=name)
                model['original'] = value['original']
                model.recipes.add(recipe)
                model.save()
        return ritem

    def parse_stock_name(self, stockname):
        p = engine()

        instruction_set = stockname.split(',')
        word_list = instruction_set[0].split(' ')
        index = 1
        categories_ignored = ['RB', 'TO']
        tokens = word_tokenize(instruction_set[0])
        tags = pos_tag(tokens)
        i=0
        while i < len(tags):
            if tags[i][1] in categories_ignored:
                index += 1
                i+= 1
            else:
                break

        quantity = word_list[index-1]
        disallowed = ['g', 'ml', 'x', 'kg', 'cups', 'cup', 'grams', 'can', 'tbsp', 'tsp', 'tbsps', 'tsps',
                 'small', 'bunch', 'piece', 'handful', 'pack', 'chopped', 'large', 'a', 'pinch',
                 'fresh', 'dried', 'heaped', 'thick', 'slices', 'slice', 'of', 'about']
        while index < len(word_list):
            if word_list[index] not in disallowed:
                break
            else:
                index+=1
        sentence = " ".join(word_list[index:])
        tokens = word_tokenize(sentence)
        categories = pos_tag(tokens)
        words = []
        for category in categories:
            if category[1] not in ['NNS', 'VBN', 'VBG']:
                words.append(category[0])
        word = " ".join(words)
        return quantity, word, None

    # def parse_stock_name(self, stockname):
    #     p = engine()
    #     souped = BeautifulSoup(stockname)
    #     stock_text = souped.get_text()
    #     words = stock_text.split(" ")
    #     indicator = 0
    #     quantity = words[indicator]
    #     pattern = re.compile('[0-9]+[a-z]*[A-Z]*')
    #     if pattern.findall(quantity):
    #         indicator = 1
    #     unit = ""
    #     units = ['g', 'ml', 'kg', 'cups', 'cup', 'grams', 'can', 'tbsp', 'tsp', 'tbsps', 'tsps',
    #              'small', 'bunch', 'piece', 'handful', 'pack', 'chopped', 'large', 'a', 'pinch',
    #              'fresh', 'dried', 'heaped', 'thick', 'slices', 'slice']
    #     words = [p.singular_noun(word) for word in words]
    #     while words[indicator] in units:
    #         unit += " "+words[indicator]
    #         indicator += 1
    #     remainder = " ".join(words[indicator:])
    #     instructions = remainder.split(",")
    #     item = instructions[0]
    #     direction = ",".join(instructions[1:])
    #
    #     return quantity, item, direction

