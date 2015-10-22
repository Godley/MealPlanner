# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from items import StockItem, RecipeItem
import sys
print sys.path
from meals.models import Stock
from scrapy.http import Request




class RecipesSpider(CrawlSpider):
    name = "recipes"
    allowed_domains = ["bbcgoodfood.com"]
    start_urls = (
        'http://www.bbcgoodfood.com/recipes/category/ingredients',
    )

    rules = (
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//li[@class="leaf link-level-3 no-sub-level"]',)), follow= True),
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//h2[@class="node-title"]',)), callback="parse_recipes_l2", follow= True),
    )


    def parse_recipes_l2(self, response):
        hxs = HtmlXPathSelector(response)
        item = RecipeItem()
        item["title"] = hxs.select("h1[@itemprop='name']/text()").extract()
        ingredients = hxs.select("//li[@itemprop='ingredients']")
        for ingredient in ingredients:
            name = hxs.select("//li[@itemprop='ingredients']/text()").extract()
            found_ingredient = Stock.objects.get(title=name)
            if found_ingredient is not None:
                found_ingredient.recipes.add(item)
                found_ingredient.save()

        yield item