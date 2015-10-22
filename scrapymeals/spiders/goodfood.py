# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from items import StockItem, RecipeItem
import sys
print sys.path
from meals.models import Stock
from scrapy.http import Request
import django




class GoodfoodSpider(CrawlSpider):
    name = "goodfood"
    allowed_domains = ["bbcgoodfood.com"]
    start_urls = (
        'http://www.bbcgoodfood.com/recipes/category/ingredients',
    )

    rules = (
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//li[@class="views-row-odd views-row-first"]','//li[@class="views-row-even"]','//li[@class="views-row-odd"]', '//li[@class="views-row-odd views-row-last"]',)), callback="parse_items", follow= True),
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//li[@class="leaf link-level-3 no-sub-level"]',)), follow= True),
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//h2[@class="node-title"]',)), callback="parse_recipes", follow= True),
    )


    def parse_recipes(self, response):
        django.setup()
        hxs = HtmlXPathSelector(response)
        item = RecipeItem()
        item["title"] = hxs.select("//title/text()").extract()
        ingredients = hxs.select("//li[@itemprop='ingredients']/text()")
        values = {}
        values["stock"] = []
        for ingredient in ingredients:
            name = ingredient.extract()
            stock_item = StockItem()
            stock_item['title'] = name
            values["stock"].append(stock_item)
        values["item"] = item
        yield values

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        titles = hxs.xpath('//span[@class="field-content"]/text()')
        items = []
        for title in titles:
            item = StockItem()
            item["title"] = title.extract()
            items.append(item)
        return(items)

