# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from items import StockItem



class GoodfoodStockSpider(CrawlSpider):
    name = "goodfood"
    allowed_domains = ["bbcgoodfood.com"]
    start_urls = (
        'http://www.bbcgoodfood.com/recipes/category/ingredients',
    )

    rules = (
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//li[@class="views-row-odd views-row-first"]','//li[@class="views-row-even"]','//li[@class="views-row-odd"]', '//li[@class="views-row-odd views-row-last"]',)), callback="parse_items", follow= True),
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//li[@class="views-row-even"]',)), callback="parse_items", follow= True)
    )

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        titles = hxs.xpath('//span[@class="field-content"]/text()')
        items = []
        for title in titles:
            item = StockItem()
            item["title"] = title.extract()
            items.append(item)
        return(items)

class GoodfoodRecipeSpider(CrawlSpider):
    name = "goodfood"
    allowed_domains = ["bbcgoodfood.com"]
    start_urls = (
        'http://www.bbcgoodfood.com/recipes/category/ingredients',
    )

    rules = (
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//li[@class="views-row-odd views-row-first"]','//li[@class="views-row-even"]','//li[@class="views-row-odd"]', '//li[@class="views-row-odd views-row-last"]',)), callback="parse_items", follow= True),
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//li[@class="views-row-even"]',)), callback="parse_items", follow= True)
    )

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        titles = hxs.xpath('//span[@class="field-content"]/text()')
        items = []
        for title in titles:
            item = StockItem()
            item["title"] = title.extract()
            items.append(item)
        return(items)