# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy_meals.items import StockItem



class GoodfoodSpider(CrawlSpider):
    name = "goodfood"
    allowed_domains = ["bbcgoodfood.com"]
    start_urls = (
        'http://www.bbcgoodfood.com/category/ingredients',
    )

    rules = (
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//li[@class="views-row-even"]','//li[@class="views-row-odd"]',)), callback="parse_items", follow= True),
    )

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        titles = hxs.xpath('//span[@class="field-content"]')
        items = []
        for titles in titles:
            item = StockItem()
            item["title"] = titles.xpath("a/text()").extract()
            item["link"] = titles.xpath("a/@href").extract()
            items.append(item)
        return items